import customtkinter
import tkinter
import cv2
from PIL import Image, ImageTk

import queue
import threading

from augmentedef import face_tracker
from augmentedef import utils
from augmentedef import face_cam_tools
from augmentedef import screen_cam_tools
from augmentedef import screen_tracker


class CameraPreview:
    def __init__(self, parent, default_index=None, run_FaceMesh=False, run_VisionLLM=False):

        self.frame = customtkinter.CTkFrame(master=parent, width=350, height=370)
        self.frame.pack_propagate(False)
        self.video_label = tkinter.Label(master=self.frame)
        self.video_label.pack(fill="both", expand=True, padx=10, pady=15)

        # Camera selection dropdown
        self.camera_var = customtkinter.StringVar()
        self.cam_selector = customtkinter.CTkComboBox(
            master=self.frame,
            values=[],
            variable=self.camera_var,
            command=self.change_camera
        )
        self.cam_selector.pack(side="bottom", pady=5, fill="both")

        self.run_FaceMesh = run_FaceMesh
        self.run_VisionLLM = run_VisionLLM
        self.cap = None
        self.current_index = default_index  # None means no device is selected initially.
        self.running = False
        self.queue = queue.Queue(maxsize=1)
        self.update_id = None
        self.paused = False
        self.thread = None  # Initialize thread attribute
        self.tracker = None

        # Add FaceTracker if using FaceMesh
        if self.run_FaceMesh:
            self.tracker = face_tracker.FaceTracker()

        if self.run_VisionLLM:
            self.tracker = screen_tracker.ScreenTracker()
            self.tracker.can_send_request = True

        self.current_rvec = None
        self.current_tvec = None

        self.refresh_camera_list()

        # Only start capture if a valid camera is selected.
        if self.current_index is not None:
            self.start_capture()

    def refresh_camera_list(self):
        # Start with "None" to indicate no selection.
        available_cams = ["None"]
        # We'll try indices 0 to 3. Adjust if you have more devices.
        for i in range(len(utils.device_names)):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # Use pygrabber device name if available; otherwise, fall back to a default name.
                if i < len(utils.device_names):
                    friendly_name = utils.device_names[i]
                else:
                    friendly_name = f"Camera {i}"
                available_cams.append(f"{i}: {friendly_name}")
                cap.release()
        self.cam_selector.configure(values=available_cams)
        self.camera_var.set("None")

    def start_capture(self):
        self.stop_capture()
        # Don't start capture if no camera is selected.
        if self.current_index is None:
            return
        self.cap = cv2.VideoCapture(self.current_index)
        self.running = True
        self.thread = threading.Thread(target=self.capture_thread, daemon=True)
        self.thread.start()
        self.update_preview()

    def capture_thread(self):
        while self.running:
            if not self.paused and self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    if self.queue.empty():
                        try:
                            self.queue.put(frame, block=False)
                        except queue.Full:
                            pass

    def update_preview(self):
        try:
            frame = self.queue.get_nowait()
            frame = cv2.resize(frame, (350, 250))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get the frame dimensions
            height, width, _ = frame.shape
            center_x, center_y = width // 2, height // 2

            # Draw a dot at the center
            cv2.circle(frame, (center_x, center_y), radius=5, color=(255, 0, 0), thickness=-1)

            if self.run_FaceMesh:
                # If this camera preview is supposed to run the face mesh estimation
                # we fire the processing of the frame
                img_tk = face_cam_tools.get_processed_frame(frame, self.tracker)
            else:
                # If this camera preview is not supposed to run the face mesh estimation
                # we send the frame as a image tk
                image = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(image=image)

            if self.run_VisionLLM and self.tracker.can_send_request and self.tracker.tracking_active:
                vision_thread = threading.Thread(target=screen_cam_tools.process_frame, args=(frame, self.tracker))
                vision_thread.start()

            self.video_label.configure(image=img_tk)
            self.video_label.image = img_tk
        except queue.Empty:
            pass

        except Exception as e:
            print(f"Something went wrong updating the preview: {e}")

        if not self.paused:
            self.update_id = self.video_label.after(42, self.update_preview)

    def change_camera(self, choice):
        if choice == "None":
            self.current_index = None
            self.stop_capture()
            return
        # Extract the index from the selection string (e.g., "1: USB Camera")
        new_index = int(choice.split(":")[0])
        if new_index != self.current_index:
            self.current_index = new_index
            self.start_capture()

    def stop_capture(self):

        try:
            if self.tracker.tracking_active is not None:
                self.tracker.tracking_active = False
        except Exception as e:
            pass
        self.running = False
        if self.cap:
            self.cap.release()
        if self.thread is not None and self.thread.is_alive():
            self.thread.join()
        if self.update_id:
            self.video_label.after_cancel(self.update_id)
        self.queue.queue.clear()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        self.update_preview()
