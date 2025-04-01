import csv
import time
from datetime import datetime


class DataRecorder:
    def __init__(self, prefix="tracking_data"):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"{prefix}_{timestamp}.csv"
        self.recording = False
        self.file = None
        self.writer = None

    def start_recording(self, prefix="tracking_data"):
        if not self.recording:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.filename = f"{prefix}_{timestamp}.csv"
            self.file = open(self.filename, mode='w', newline='')
            self.writer = csv.writer(self.file)

            # Writing header
            self.writer.writerow([
                "Timestamp", "FaceCam Status", "FaceCam Task Status",
                "FaceCam_T_X", "FaceCam_T_Y", "FaceCam_T_Z",
                "FaceCam_R_X", "FaceCam_R_Y", "FaceCam_R_Z", "FaceCam OffTask Time",
                "ScreenCam Status", "ScreenCam Task Status", "ScreenCam Latency", "ScreenCam Last Return Reason", "ScreenCam OffTask Time",
                "SilversModel Task Status", "SilversModel Output", "SilversModel OffTask Time"

            ])
            self.recording = True
            print(f"Recording started, saving to {self.filename}")

    def stop_recording(self):
        if self.recording:
            self.file.close()
            self.recording = False
            print(f"Recording stopped. Data saved to {self.filename}")

    def log_data(self, cam1_preview, cam2_preview, silversModel_status, silversModel_Output, silversModelOffTaskTime):
        if self.recording and self.writer:
            self.writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Active" if cam1_preview.tracker.tracking_active else "Not Active",
                "ON TASK" if cam1_preview.tracker.on_task and cam1_preview.tracker.tracking_active else "OFF TASK",
                cam1_preview.tracker.smoothed_position[0] if cam1_preview.tracker.smoothed_position is not None else 0.0,
                cam1_preview.tracker.smoothed_position[1] if cam1_preview.tracker.smoothed_position is not None else 0.0,
                cam1_preview.tracker.smoothed_position[2] if cam1_preview.tracker.smoothed_position is not None else 0.0,
                cam1_preview.tracker.smoothed_angles[0] if cam1_preview.tracker.smoothed_angles is not None else 0.0,
                cam1_preview.tracker.smoothed_angles[1] if cam1_preview.tracker.smoothed_angles is not None else 0.0,
                cam1_preview.tracker.smoothed_angles[2] if cam1_preview.tracker.smoothed_angles is not None else 0.0,
                cam1_preview.tracker.offTask_currentTime,
                "Active" if cam2_preview.tracker.tracking_active else "Not Active",
                "ON TASK" if cam2_preview.tracker.on_task and cam2_preview.tracker.tracking_active is not None else "OFF TASK",
                cam2_preview.tracker.last_vision_llm_latency if cam2_preview.tracker.tracking_active is not None else 0.0,
                cam2_preview.tracker.last_vision_reason if cam2_preview.tracker.tracking_active is not None else "None",
                cam2_preview.tracker.offTask_currentTime,
                "On Task" if silversModel_status else "Off Task", silversModel_Output, silversModelOffTaskTime

            ])
