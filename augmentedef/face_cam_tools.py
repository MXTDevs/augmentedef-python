import cv2
import mediapipe as mp
import numpy as np
from PIL import ImageTk
from PIL import Image

from augmentedef import utils
from augmentedef import face_tracker

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Camera parameters
IMAGE_WIDTH = 350
IMAGE_HEIGHT = 250
CAMERA_FOV = 60

# Face mesh configuration
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Camera matrix calculation using FOV
focal_length = IMAGE_WIDTH / (2 * np.tan(np.deg2rad(CAMERA_FOV / 2)))
camera_matrix = np.array([
    [focal_length, 0, IMAGE_WIDTH / 2],
    [0, focal_length, IMAGE_HEIGHT / 2],
    [0, 0, 1]
], dtype=np.float64)

# Smoothing buffers (using a moving average over 5 frames)
angle_buffer = np.zeros((5, 3))
translation_buffer = np.zeros((5, 3))
buffer_index = 0

# Define axis length (in the same metric as your 3D model, e.g. centimeters)
axis_length = 0.2 # You can adjust this value


def get_processed_frame(inputFrame, tracker: face_tracker.FaceTracker()):
    frame = inputFrame
    frame_rgb = inputFrame

    if tracker.tracking_active is False:
        image = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=image)
        return imgtk

    # Use a fixed set of stable landmark indices for calibration:
    # These indices are chosen based on stable facial features (eyes, nose, mouth, chin)
    calibration_indices = [33, 263, 1, 61, 291, 199, 10, 107, 336, 296, 454]

    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks and tracker.tracking_active:
        face_landmarks = results.multi_face_landmarks[0]
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
        )

        # Convert landmark positions to pixel coordinates
        current_points = {}
        for idx, landmark in enumerate(face_landmarks.landmark):
            x = int(landmark.x * IMAGE_WIDTH)
            y = int(landmark.y * IMAGE_HEIGHT)
            current_points[idx] = (x, y)

        # Calibration phase: when tracking is activated and model is not yet built
        if tracker.tracking_active and tracker.model_points_3d is None:
            # Ensure that the face landmarks for the fixed indices are available
            if all(idx in current_points for idx in calibration_indices):
                model_points_3d_list = []

                # Calculate scale factor using eye distance (landmarks 33 and 263)
                left_eye = face_landmarks.landmark[33]
                right_eye = face_landmarks.landmark[263]
                eye_distance = np.sqrt(
                    (left_eye.x - right_eye.x) ** 2 +
                    (left_eye.y - right_eye.y) ** 2
                ) * IMAGE_WIDTH

                # Convert to metric space using average inter-pupillary distance (~6.4cm)
                scale_factor = 0.064 / eye_distance

                # Build 3D model from the selected stable landmarks
                for idx in calibration_indices:
                    landmark = face_landmarks.landmark[idx]
                    x = (landmark.x - 0.5) * IMAGE_WIDTH * scale_factor
                    y = (landmark.y - 0.5) * IMAGE_HEIGHT * scale_factor
                    z = landmark.z * IMAGE_WIDTH * scale_factor
                    model_points_3d_list.append([x, y, z])

                tracker.model_points_3d = np.array(model_points_3d_list, dtype=np.float64)
                print(f"Calibration complete with {len(tracker.model_points_3d)} points.")

        # Tracking phase: once calibrated
        if tracker.tracking_active and tracker.model_points_3d is not None:

            # Collect correspondences for the fixed calibration indices
            object_points = []
            image_points = []
            for idx in calibration_indices:
                if idx in current_points:
                    object_points.append(tracker.model_points_3d[calibration_indices.index(idx)])
                    image_points.append(current_points[idx])
            object_points = np.array(object_points, dtype=np.float64)
            image_points = np.array(image_points, dtype=np.float64)

            # Use solvePnPRansac for robust pose estimation
            if len(object_points) >= 4:
                retval, tracker.rvec, tracker.tvec, inliers = cv2.solvePnPRansac(
                    objectPoints=object_points,
                    imagePoints=image_points,
                    cameraMatrix=camera_matrix,
                    distCoeffs=None,
                    iterationsCount=100,
                    reprojectionError=8.0,
                    confidence=0.99,
                    flags=cv2.SOLVEPNP_ITERATIVE
                )

                if retval and inliers is not None and len(inliers) > 0:
                    # Convert rotation vector to rotation matrix
                    R_mat, _ = cv2.Rodrigues(tracker.rvec)

                    # Calculate relative transformation from a base pose
                    rel_rotation = R_mat @ tracker.base_rotation.T
                    rel_translation = (
                                                  tracker.tvec.flatten() - tracker.base_translation) * 100  # Convert to centimeters

                    # Convert relative rotation back to rotation vector and then to Euler angles
                    rel_rvec, _ = cv2.Rodrigues(rel_rotation)
                    pitch, yaw, roll = utils.rotation_vector_to_euler(rel_rvec)

                    # Apply smoothing using a moving average filter
                    tracker.smoothed_angles = utils.smooth_values(tracker.angle_buffer, [pitch, yaw, roll],
                                                          tracker.buffer_index)
                    tracker.smoothed_position = utils.smooth_values(tracker.translation_buffer, rel_translation,
                                                            tracker.buffer_index)

                    tracker.on_task = tracker.update_on_task_status()


                    '''
                    # Overlay the pose data on the frame
                    cv2.putText(frame,
                                f"Rotation: Pitch={tracker.smoothed_angles[0]:.1f}deg, Yaw={tracker.smoothed_angles[1]:.1f}deg, Roll={tracker.smoothed_angles[2]:.1f}deg",
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
                    cv2.putText(frame,
                                f"Position: X={tracker.smoothed_position[0]:.1f}cm, Y={tracker.smoothed_position[1]:.1f}cm, Z={tracker.smoothed_position[2]:.1f}cm",
                                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 2)
                    '''

                    # ----- Improved Axis Visualization -----
                    # First, project the origin (face center) to image space.
                    origin_3d = np.array([[0, 0, 0]], dtype=np.float32)
                    origin_img = cv2.projectPoints(origin_3d, tracker.rvec, tracker.tvec, camera_matrix, None)[0][
                        0].ravel()

                    # For each axis, we define the vector in face model space.
                    # Then we check if its projection goes in the positive direction relative to origin.

                    # X-axis (red): desired to go rightwards on the image
                    axis_x = np.array([0, 0, axis_length], dtype=np.float32)
                    proj_x = cv2.projectPoints(np.array([axis_x]), tracker.rvec, tracker.tvec, camera_matrix, None)[0][
                        0].ravel()

                    # Y-axis (green): desired to go downward on the image
                    axis_y = np.array([0, axis_length, 0], dtype=np.float32)
                    proj_y = cv2.projectPoints(np.array([axis_y]), tracker.rvec, tracker.tvec, camera_matrix, None)[0][
                        0].ravel()

                    # Z-axis (blue): we want it to point forward (away from the face) in camera space.
                    axis_z = np.array([axis_length, 0, 0], dtype=np.float32)
                    # Compute the endpoint in camera coordinates
                    proj_z = cv2.projectPoints(np.array([axis_z]), tracker.rvec, tracker.tvec, camera_matrix, None)[0][
                        0].ravel()

                    # Draw the axes starting from the projected origin.
                    origin_pt = tuple(origin_img.astype(int))
                    cv2.line(frame, origin_pt, tuple(proj_x.astype(int)), (0, 0, 255), 3)  # X-axis in red
                    cv2.line(frame, origin_pt, tuple(proj_y.astype(int)), (0, 255, 0), 3)  # Y-axis in green
                    cv2.line(frame, origin_pt, tuple(proj_z.astype(int)), (255, 0, 0), 3)  # Z-axis in blue
                    # -----------------------------------------
    image = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=image)
    return imgtk
