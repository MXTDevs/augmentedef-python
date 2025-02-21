import customtkinter
import tkinter as tk

import os
import ctypes

from augmentedef import camera_preview
from augmentedef import data_recorder

recorder = data_recorder.DataRecorder()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("800x900")
root.resizable(False, True)
# 🏷 Change Window Title
root.title("Augmented EF")

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ICON_PATH = os.path.join(ROOT_DIR, "augmentedef_icon.ico")

# For .ico files (Windows)
root.iconbitmap(ICON_PATH)

# Change taskbar icon (Windows only)
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Augmented EF")

# UI Elements
PreviewsFrame = customtkinter.CTkFrame(master=root)
PreviewsFrame.pack(side="top", pady=10, padx=20, fill="both", expand=False)

FaceCamFrame = customtkinter.CTkFrame(master=PreviewsFrame, width=350, height=250)
FaceCamLabel = customtkinter.CTkLabel(master=FaceCamFrame, text="FaceCam Preview")
FaceCamLabel.pack(expand=True)
cam1_preview = camera_preview.CameraPreview(
    FaceCamFrame,
    default_index=None,
    run_FaceMesh=True,
    run_VisionLLM=False
)
cam1_preview.frame.pack(fill="both", side="left", expand=True)

ScreenCamFrame = customtkinter.CTkFrame(master=PreviewsFrame, width=350, height=250)
ScreenCamLabel = customtkinter.CTkLabel(master=ScreenCamFrame, text="ScreenCam Preview")
ScreenCamLabel.pack(expand=True)
cam2_preview = camera_preview.CameraPreview(
    ScreenCamFrame,
    default_index=None,
    run_FaceMesh=False,
    run_VisionLLM=True
)
cam2_preview.frame.pack(fill="both", side="left", expand=True)

PreviewsFrame.columnconfigure(0, weight=0)
PreviewsFrame.columnconfigure(0, weight=0)
PreviewsFrame.rowconfigure(0, weight=1)
PreviewsFrame.rowconfigure(0, weight=0)

FaceCamFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
ScreenCamFrame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

MainControlsFrame = customtkinter.CTkScrollableFrame(master=root, height=100)
MainControlsFrame.pack(side="left", anchor="w", pady=(5, 20), padx=(20, 10), fill="both", expand=True)

FaceCamControlsLabel = customtkinter.CTkLabel(master=MainControlsFrame, text="FACECAM OPTIONS",
                                              font=("Segoe UI", 14, "bold"))
FaceCamControlsLabel.pack(padx=10, pady=(0, 10), side="top", anchor="w")

labelMaxDistanceOnTask = customtkinter.CTkLabel(master=MainControlsFrame, text="Max Distance On Task")
labelMaxDistanceOnTask.pack(padx=10, pady=(0, 0), side="top", anchor="w")

entryMaxDistanceOnTask = customtkinter.CTkEntry(master=MainControlsFrame, placeholder_text="15")
entryMaxDistanceOnTask.pack(padx=10, pady=(0, 5), side="top", anchor="w")

labelMaxYawOnTask = customtkinter.CTkLabel(master=MainControlsFrame, text="Max Yaw On Task")
labelMaxYawOnTask.pack(padx=10, pady=(0, 0), side="top", anchor="w")

entryMaxYawOnTask = customtkinter.CTkEntry(master=MainControlsFrame, placeholder_text="25")
entryMaxYawOnTask.pack(padx=10, pady=(0, 5), side="top", anchor="w")

labelMaxPitchOnTask = customtkinter.CTkLabel(master=MainControlsFrame, text="Max Pitch On Task")
labelMaxPitchOnTask.pack(padx=10, pady=(0, 0), side="top", anchor="w")

entryMaxPitchOnTask = customtkinter.CTkEntry(master=MainControlsFrame, placeholder_text="30")
entryMaxPitchOnTask.pack(padx=10, pady=(0, 5), side="top", anchor="w")

faceCamButtonsFrame = customtkinter.CTkFrame(master=MainControlsFrame)
faceCamButtonsFrame.pack(side="top", anchor="n", fill="x")

buttonSetReferenceTracking = customtkinter.CTkButton(master=faceCamButtonsFrame, text="Set Face",
                                                     command=lambda: start_tracking_facecam_with_values(), width=100)
buttonSetReferenceTracking.pack(side="left", padx=5, pady=(5, 5), anchor="w")

buttonSetOffsetOrigin = customtkinter.CTkButton(master=faceCamButtonsFrame, text="Set Offset",
                                                command=lambda: cam1_preview.tracker.reset_origin(), width=100)
buttonSetOffsetOrigin.pack(side="left", padx=5, pady=(5, 5), anchor="w")

buttonStopTrackingFaceCam = customtkinter.CTkButton(master=faceCamButtonsFrame, text="Stop Tracking",
                                                command=lambda: cam1_preview.tracker.stop_tracking(), width=100)
buttonStopTrackingFaceCam.pack(side="left", padx=5, pady=(5, 5), anchor="w")

FaceCamControlsLabel = customtkinter.CTkLabel(master=MainControlsFrame, text="SCREENCAM OPTIONS",
                                              font=("Segoe UI", 14, "bold"))
FaceCamControlsLabel.pack(padx=10, pady=(5, 5), side="top", anchor="w")

# labelAdditionalDelay = customtkinter.CTkLabel(master=MainControlsFrame, text="Additional Delay")
# labelAdditionalDelay.pack(padx=10, pady=(0, 0), side="top", anchor="w")

# entryAdditionalDelay = customtkinter.CTkEntry(master=MainControlsFrame, placeholder_text="Additional Delay")
# entryAdditionalDelay.pack(padx=10, pady=(0, 5), side="top", anchor="w")

# labelSystemPrompt = customtkinter.CTkLabel(master=MainControlsFrame, text="System Prompt")
# labelSystemPrompt.pack(padx=10, pady=(0, 0), side="top", anchor="w")

# entrySystemPrompt = customtkinter.CTkEntry(master=MainControlsFrame, placeholder_text="System Prompt")
# entrySystemPrompt.pack(padx=10, pady=(0, 5), side="top", anchor="w", fill="x")

FaceCamButtonsFrame = customtkinter.CTkFrame(master=MainControlsFrame)
FaceCamButtonsFrame.pack(side="top", anchor="w")

buttonStartSendingRequest = customtkinter.CTkButton(master=FaceCamButtonsFrame, text="Start Sending Requests",
                                                    command=lambda: cam2_preview.tracker.start_tracking())
buttonStartSendingRequest.pack(side="left", padx=10, pady=(0, 5), anchor="w")

buttonStopSendingRequest = customtkinter.CTkButton(master=FaceCamButtonsFrame, text="Stop Sending Requests",
                                                   command=lambda: cam2_preview.tracker.stop_tracking())
buttonStopSendingRequest.pack(side="left", padx=10, pady=(0, 5), anchor="w")

FaceCamControlsLabel = customtkinter.CTkLabel(master=MainControlsFrame, text="GENERAL OPTIONS",
                                              font=("Segoe UI", 14, "bold"))
FaceCamControlsLabel.pack(padx=10, pady=(5, 0), side="top", anchor="w")

labelSessionID = customtkinter.CTkLabel(master=MainControlsFrame, text="Session ID")
labelSessionID.pack(padx=10, pady=(0, 0), side="top", anchor="w")

entrySessionID = customtkinter.CTkEntry(master=MainControlsFrame, placeholder_text="Session Identifier")
entrySessionID.pack(padx=10, pady=(0, 5), side="top", anchor="w")

generalButtonsFrame = customtkinter.CTkFrame(master=MainControlsFrame)
generalButtonsFrame.pack(side="top", anchor="w")



buttonStartRecordingData = customtkinter.CTkButton(master=generalButtonsFrame, text="Start Recording Data",
                                                   command=lambda: start_recording_with_sessionID())
buttonStartRecordingData.pack(pady=5, padx=10, side="left", anchor="w")

buttonStartRecordingData = customtkinter.CTkButton(master=generalButtonsFrame, text="Stop Recording Data",
                                                   command=lambda: recorder.stop_recording())
buttonStartRecordingData.pack(pady=5, padx=10, side="left", anchor="w")

DataFrame = customtkinter.CTkScrollableFrame(master=root)
DataFrame.pack(side="left", anchor="e", pady=(5, 20), padx=(10, 20), fill="both", expand=True)

DataLogLabel = customtkinter.CTkLabel(master=DataFrame, text="FACECAM DATA LOG", font=("Segoe UI", 14, "bold"))
DataLogLabel.pack(padx=10, pady=(0, 10), side="top", anchor="n")

FaceCamStatusLabel = customtkinter.CTkLabel(master=DataFrame, text="STATUS: Not Active, Set Reference Tracking")
FaceCamStatusLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

FaceCamTaskStatusLabel = customtkinter.CTkLabel(master=DataFrame, text="TASK STATUS: OFF TASK")
FaceCamTaskStatusLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

FaceCamTVectorLabel = customtkinter.CTkLabel(master=DataFrame, text="Translation Vector : X=00 Y=00 Z=00")
FaceCamTVectorLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

FaceCamRVectorLabel = customtkinter.CTkLabel(master=DataFrame, text="Rotation Vector : X=00 Y=00 Z=00")
FaceCamRVectorLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

# FaceCamRQuaternionLabel = customtkinter.CTkLabel(master=DataFrame, text="Rotation Quaternion : X=00 Y=00 Z=00 W=00")
# FaceCamRQuaternionLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

DataLogLabel = customtkinter.CTkLabel(master=DataFrame, text="SCREENCAM DATA LOG", font=("Segoe UI", 14, "bold"))
DataLogLabel.pack(padx=10, pady=(10, 10), side="top", anchor="n")

ScreenCamStatusLabel = customtkinter.CTkLabel(master=DataFrame, text="STATUS: Not Active, Start Sending Requests")
ScreenCamStatusLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

ScreenCamTaskStatus = customtkinter.CTkLabel(master=DataFrame, text="TASK STATUS: OFF TASK")
ScreenCamTaskStatus.pack(padx=10, pady=(0, 0), side="top", anchor="w")

ScreenCamLatencyResponse = customtkinter.CTkLabel(master=DataFrame, text="LAST REQ LATENCY: 00s")
ScreenCamLatencyResponse.pack(padx=10, pady=(0, 0), side="top", anchor="w")

ScreenCamLastReturnReasonFrame = customtkinter.CTkFrame(master=DataFrame)
ScreenCamLastReturnReasonFrame.pack(side="top", anchor="w", fill="both", expand=True)

ScreenCamLastReturnReason = customtkinter.CTkLabel(master=ScreenCamLastReturnReasonFrame, text="LAST REQ REASON: None",
                                                   wraplength=300, anchor="w")
ScreenCamLastReturnReason.grid(row=0, column=0, sticky="nswe", padx=10, pady=(0, 5), columnspan=1)

# ScreenCamLastReceiveResult = customtkinter.CTkLabel(master=DataFrame, text="LAST REC RESULT: None")
# ScreenCamLastReceiveResult.pack(padx=10, pady=(0, 0), side="top", anchor="w")

GeneralDataLogLabel = customtkinter.CTkLabel(master=DataFrame, text="GENERAL DATA LOG", font=("Segoe UI", 14, "bold"))
GeneralDataLogLabel.pack(padx=10, pady=(0, 10), side="top", anchor="n")

GeneralStatusLabel = customtkinter.CTkLabel(master=DataFrame, text="Status: Not recording")
GeneralStatusLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")


# Handle window focus events
def on_focus_in(event):
    pass
    # cam1_preview.resume()
    # cam2_preview.resume()


def on_focus_out(event):
    pass
    # cam1_preview.pause()
    # cam2_preview.pause()


# root.bind("<FocusIn>", on_focus_in)
# root.bind("<FocusOut>", on_focus_out)


# Handle window close
def on_closing():
    cam1_preview.stop_capture()
    cam2_preview.stop_capture()
    root.destroy()


def start_tracking_facecam_with_values():
    try:
        newMaxDistance = int(entryMaxDistanceOnTask.get().strip())
        newMaxYaw = int(entryMaxYawOnTask.get().strip())
        newMaxPitch = int(entryMaxPitchOnTask.get().strip())
    except Exception:
        newMaxDistance = 0
        newMaxYaw = 0
        newMaxPitch = 0

    cam1_preview.tracker.start_tracking(newMaxDistance, newMaxYaw, newMaxPitch)

def start_recording_with_sessionID():
    sessionID = entrySessionID.get()
    recorder.start_recording(sessionID)


def update_data_log():
    # Updating the FaceCam Status
    if cam1_preview.tracker.tracking_active:
        FaceCamStatusLabel.configure(text="STATUS: Active")
    else:
        FaceCamStatusLabel.configure(text="STATUS: Not Active, Set Face Reference")

    # Updating FaceCam Task Status
    if cam1_preview.tracker.on_task and cam1_preview.tracker.tracking_active:
        FaceCamTaskStatusLabel.configure(text="TASK STATUS: ON TASK", font=("Segoe UI", 14, "bold"), text_color="green")
    else:
        FaceCamTaskStatusLabel.configure(text="TASK STATUS: OFF TASK", font=("Segoe UI", 14, "bold"), text_color="red")

    # Updating the FaceCam Translation Vector
    if cam1_preview.tracker.smoothed_position is not None and cam1_preview.tracker.tracking_active:
        FaceCamTVectorLabel.configure(
            text="Translation Vector: " +
                 "X: " + str(round(cam1_preview.tracker.smoothed_position[0], 2)) + " "
                                                                                    "Y: " + str(
                round(cam1_preview.tracker.smoothed_position[1], 2)) + " "
                                                                       "Z: " + str(
                round(cam1_preview.tracker.smoothed_position[2], 2))
        )
    else:
        FaceCamTVectorLabel.configure(text="Translation Vector : X=0.00 Y=0.00 Z=0.00")

    # Updating the FaceCam Rotation Vector
    if cam1_preview.tracker.smoothed_angles is not None and cam1_preview.tracker.tracking_active:
        FaceCamRVectorLabel.configure(
            text="Rotation Vector: " +
                 "X: " + str(round(cam1_preview.tracker.smoothed_angles[0], 2)) + " "
                                                                                  "Y: " + str(
                round(cam1_preview.tracker.smoothed_angles[1], 2)) + " "
                                                                     "Z: " + str(
                round(cam1_preview.tracker.smoothed_angles[2], 2))
        )
    else:
        FaceCamRVectorLabel.configure(text="Rotation Vector : X=0.00 Y=0.00 Z=0.00")

    # Updating ScreenCam Status
    if cam2_preview.tracker.tracking_active:
        ScreenCamStatusLabel.configure(text="STATUS: Active")
    else:
        ScreenCamStatusLabel.configure(text="STATUS: Not Active, Start Sending Requests")

    # Updating ScreenCam Task Status
    if cam2_preview.tracker.on_task and cam2_preview.tracker.tracking_active:
        ScreenCamTaskStatus.configure(text="TASK STATUS: ON TASK", font=("Segoe UI", 14, "bold"), text_color="green")
    else:
        ScreenCamTaskStatus.configure(text="TASK STATUS: OFF TASK", font=("Segoe UI", 14, "bold"), text_color="red")

    # Updating ScreenCam Latency Response
    if cam2_preview.tracker.tracking_active:
        ScreenCamLatencyResponse.configure(
            text="LAST REQ LATENCY: " + str(round(cam2_preview.tracker.last_vision_llm_latency, 2)) + "s")
    else:
        ScreenCamLatencyResponse.configure(text="LAST REQ LATENCY: 00s")

    # Updating ScreenCam Last Return Reason
    if cam2_preview.tracker.tracking_active:
        ScreenCamLastReturnReason.configure(text="LAST REQ REASON: " + cam2_preview.tracker.last_vision_reason)
    else:
        ScreenCamLastReturnReason.configure(text="LAST REQ REASON: None")

    # Updating general recording status
    if recorder.recording:
        GeneralStatusLabel.configure(text="Recording...", font=("Segoe UI", 14, "bold"), text_color="green")
    else:
        GeneralStatusLabel.configure(text="Not recording...", font=("Segoe UI", 14, "bold"), text_color="red")

    recorder.log_data(cam1_preview, cam2_preview)

    root.after(100, update_data_log)


update_data_log()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
