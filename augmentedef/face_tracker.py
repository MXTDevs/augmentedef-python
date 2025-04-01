import cv2
import numpy as np


class FaceTracker:
    def __init__(self):
        self.tracking_active = False
        self.model_points_3d = None
        self.base_rotation = np.eye(3)
        self.base_translation = np.zeros(3)
        self.angle_buffer = np.zeros((10, 3))  # Example buffer
        self.translation_buffer = np.zeros((10, 3))
        self.buffer_index = 0
        self.tvec = None
        self.rvec = None
        self.smoothed_position = np.zeros(3)
        self.smoothed_angles = np.zeros(3)
        self.on_task = False
        self.max_distance_on_task = 15
        self.max_yaw_on_task = 25
        self.max_pitch_on_task = 30
        self.offTask_currentTime = 0

    def start_tracking(self, new_max_distance_on_task, new_max_yaw_on_task, new_max_pitch_on_task):

        if new_max_distance_on_task > 0:
            self.max_distance_on_task = new_max_distance_on_task

        if new_max_yaw_on_task > 0:
            self.max_yaw_on_task = new_max_yaw_on_task

        if new_max_pitch_on_task > 0:
            self.max_pitch_on_task = new_max_pitch_on_task

        self.tracking_active = True
        self.model_points_3d = None  # Force re-calibration
        print("Starting calibration... please face the camera directly.")

    def stop_tracking(self):
        self.tracking_active = False
        self.model_points_3d = None
        self.base_rotation = np.eye(3)
        self.base_translation = np.zeros(3)
        self.angle_buffer = np.zeros((10, 3))  # Example buffer
        self.translation_buffer = np.zeros((10, 3))
        self.buffer_index = 0
        self.tvec = None
        self.rvec = None
        self.smoothed_position = None
        self.smoothed_angles = None

    def reset_origin(self):

        try:
            self.base_translation = self.tvec.flatten()
            self.base_rotation, _ = cv2.Rodrigues(self.rvec)
            print("Origin reset to current position.")
        except Exception:
            print("Failed to reset origin, check if the source is valid")

    def update_on_task_status(self):

        if abs(self.smoothed_angles[0]) > self.max_pitch_on_task:
            return False

        if abs(self.smoothed_angles[1]) > self.max_yaw_on_task:
            return False

        if abs(self.smoothed_position[0]) > self.max_distance_on_task:
            return False

        if abs(self.smoothed_position[1]) > self.max_distance_on_task:
            return False

        if abs(self.smoothed_position[2]) > self.max_distance_on_task:
            return False

        return True
