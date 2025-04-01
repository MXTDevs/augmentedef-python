import customtkinter
import tkinter as tk
import tkinter.filedialog as fd
import pygame

import os
import ctypes

from augmentedef import camera_preview
from augmentedef import data_recorder
from augmentedef import silvers_model_tools

# Initialize pygame mixer
pygame.mixer.init()

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

AudioInterventionOptionsLabel = customtkinter.CTkLabel(master=MainControlsFrame, text="AUDIO INTERVENTION OPTIONS",
                                                       font=("Segoe UI", 14, "bold"))
AudioInterventionOptionsLabel.pack(padx=10, pady=(5, 0), side="top", anchor="w")

labelOfftaskTimeout = customtkinter.CTkLabel(master=MainControlsFrame, text="Off Task Timeout")
labelOfftaskTimeout.pack(padx=10, pady=(0, 0), side="top", anchor="w")

entryOfftaskTimeout = customtkinter.CTkEntry(master=MainControlsFrame, placeholder_text="10")
entryOfftaskTimeout.pack(padx=10, pady=(0, 5), side="top", anchor="w")

# Offtask Criteria Label
labelOfftaskCriteria = customtkinter.CTkLabel(master=MainControlsFrame, text="Off Task Criteria")
labelOfftaskCriteria.pack(padx=10, pady=(5, 0), side="top", anchor="w")

# Checkboxes for FaceCam and ScreenCam
checkboxFaceCam = customtkinter.CTkCheckBox(master=MainControlsFrame, text="FaceCam")
checkboxFaceCam.pack(padx=10, pady=(0, 0), side="top", anchor="w")

checkboxScreenCam = customtkinter.CTkCheckBox(master=MainControlsFrame, text="ScreenCam")
checkboxScreenCam.pack(padx=10, pady=(0, 5), side="top", anchor="w")

checkboxSilversModel = customtkinter.CTkCheckBox(master=MainControlsFrame, text="SilversModel")
checkboxSilversModel.pack(padx=10, pady=(0, 5), side="top", anchor="w")

# Intervention Volume Label
# labelInterventionVolume = customtkinter.CTkLabel(master=MainControlsFrame, text="Intervention Volume")
# labelInterventionVolume.pack(padx=10, pady=(5, 0), side="top", anchor="w")

# Frame to hold slider and value label
# frameIntervention = customtkinter.CTkFrame(master=MainControlsFrame)
# frameIntervention.pack(padx=10, pady=(0, 5), side="top", anchor="w", fill="x")

# Slider for Intervention Volume (0 to 10) with lambda
# sliderInterventionVolume = customtkinter.CTkSlider(master=frameIntervention, from_=0, to=10, command=lambda value: update_slider_value(value))
# sliderInterventionVolume.pack(padx=(0, 5), pady=0, side="left", expand=True, fill="x")

# Label to show the slider value
#labelVolumeValue = customtkinter.CTkLabel(master=frameIntervention, text="0")  # Default value
#labelVolumeValue.pack(padx=(5, 0), pady=0, side="right")

# Audio File Label
labelAudioFile = customtkinter.CTkLabel(master=MainControlsFrame, text="Audio File")
labelAudioFile.pack(padx=10, pady=(5, 0), side="top", anchor="w")

# Frame for Entry and Button
frameAudioFile = customtkinter.CTkFrame(master=MainControlsFrame)
frameAudioFile.pack(padx=10, pady=(0, 5), side="top", anchor="w", fill="x")

# Entry for Audio File Path
entryAudioFile = customtkinter.CTkEntry(master=frameAudioFile, placeholder_text="Select an audio file")
entryAudioFile.pack(padx=(0, 5), pady=0, side="left", expand=True, fill="x")

# Browse Button
buttonBrowseAudio = customtkinter.CTkButton(master=frameAudioFile, text="Browse", width=80,
                                            command=lambda: browse_audio_file())
buttonBrowseAudio.pack(padx=(5, 0), pady=0, side="right")

DataFrame = customtkinter.CTkScrollableFrame(master=root)
DataFrame.pack(side="left", anchor="e", pady=(5, 20), padx=(10, 20), fill="both", expand=True)

FaceCamDataLogLabel = customtkinter.CTkLabel(master=DataFrame, text="FACECAM DATA LOG", font=("Segoe UI", 14, "bold"))
FaceCamDataLogLabel.pack(padx=10, pady=(0, 10), side="top", anchor="n")

FaceCamStatusLabel = customtkinter.CTkLabel(master=DataFrame, text="STATUS: Not Active, Set Reference Tracking")
FaceCamStatusLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

FaceCamTaskStatusLabel = customtkinter.CTkLabel(master=DataFrame, text="TASK STATUS: OFF TASK")
FaceCamTaskStatusLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

FaceCamTVectorLabel = customtkinter.CTkLabel(master=DataFrame, text="Translation Vector : X=00 Y=00 Z=00")
FaceCamTVectorLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

FaceCamRVectorLabel = customtkinter.CTkLabel(master=DataFrame, text="Rotation Vector : X=00 Y=00 Z=00")
FaceCamRVectorLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

FaceCamOffTaskTime = customtkinter.CTkLabel(master=DataFrame, text="FaceCam Off Task time: 0")
FaceCamOffTaskTime.pack(padx=10, pady=(0, 0), side="top", anchor="w")

# FaceCamRQuaternionLabel = customtkinter.CTkLabel(master=DataFrame, text="Rotation Quaternion : X=00 Y=00 Z=00 W=00")
# FaceCamRQuaternionLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

SilversModelDataLogLabel = customtkinter.CTkLabel(master=DataFrame, text="SILVER MODEL DATA LOG",
                                                  font=("Segoe UI", 14, "bold"))
SilversModelDataLogLabel.pack(padx=10, pady=(10, 10), side="top", anchor="n")

SilverModelStatusLabel = customtkinter.CTkLabel(master=DataFrame, text="STATUS: Not Active, Set Reference Tracking")
SilverModelStatusLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

SilverModelTaskStatusLabel = customtkinter.CTkLabel(master=DataFrame, text="TASK STATUS: OFF TASK")
SilverModelTaskStatusLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

SilverModelOutputLabel = customtkinter.CTkLabel(master=DataFrame, text="MODEL OUTPUT: 0")
SilverModelOutputLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")

SilverModelOffTaskTime = customtkinter.CTkLabel(master=DataFrame, text="FaceCam Off Task time: 0")
SilverModelOffTaskTime.pack(padx=10, pady=(0, 0), side="top", anchor="w")

ScreenCamDataLogLabel = customtkinter.CTkLabel(master=DataFrame, text="SCREENCAM DATA LOG",
                                               font=("Segoe UI", 14, "bold"))
ScreenCamDataLogLabel.pack(padx=10, pady=(10, 10), side="top", anchor="n")

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

ScreenCamOffTaskTime = customtkinter.CTkLabel(master=DataFrame, text="ScreenCam Off Task time: 0")
ScreenCamOffTaskTime.pack(padx=10, pady=(0, 0), side="top", anchor="w")

# ScreenCamLastReceiveResult = customtkinter.CTkLabel(master=DataFrame, text="LAST REC RESULT: None")
# ScreenCamLastReceiveResult.pack(padx=10, pady=(0, 0), side="top", anchor="w")

GeneralDataLogLabel = customtkinter.CTkLabel(master=DataFrame, text="GENERAL DATA LOG", font=("Segoe UI", 14, "bold"))
GeneralDataLogLabel.pack(padx=10, pady=(0, 10), side="top", anchor="n")

GeneralStatusLabel = customtkinter.CTkLabel(master=DataFrame, text="Status: Not recording")
GeneralStatusLabel.pack(padx=10, pady=(0, 0), side="top", anchor="w")


# Function to update the label when the slider moves
def update_slider_value(value):
    pass
    #labelVolumeValue.configure(text=f"{int(float(value))}")  # Convert value to integer


# Function to browse and select an audio file
def browse_audio_file():
    global audio_path
    file_path = fd.askopenfilename(filetypes=[("WAV Audio Files", "*.wav")])  # Restrict to .wav files
    if file_path:  # If a file is selected, update the entry field
        entryAudioFile.delete(0, "end")
        entryAudioFile.insert(0, file_path)
        audio_path = file_path


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


screenCam_OffTask_CurrentTime = 0
faceCam_OffTask_CurrentTime = 0
silversModel_OffTask_CurrentTime = 0
silversModel_OnTask = False

audio_intervention_playing = False  # Track if the audio is playing
audio_path = "audio_file.mp3"  # Replace with actual file path

OffTask_Timeout_Value = 10
Model_prediction_output = 0


def refresh_audio_intervention():
    global audio_intervention_playing

    # If FaceCam criteria is True and Face Cam Off Task is more than 10 seconds
    # OR If ScreenCam criteria is True and Screen Cam Off Task time is more than 10 seconds
    # AND Audio Intervention is not already playing AND Audio Path is not None
    if (((checkboxFaceCam.get() and faceCam_OffTask_CurrentTime > OffTask_Timeout_Value) or
         (checkboxScreenCam.get() and screenCam_OffTask_CurrentTime > OffTask_Timeout_Value) or
         (checkboxSilversModel.get() and silversModel_OffTask_CurrentTime > OffTask_Timeout_Value)) and not audio_intervention_playing and audio_path):
        # Play Audio Intervention in Loop
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play(-1)  # -1 makes it loop indefinitely
        audio_intervention_playing = True

    # If FaceCam criteria is True and Face Cam Off task is less than 10 seconds
    # OR If ScreenCam criteria is True and Screen Cam Off Task time is less than 10 seconds
    # Stop Playing Audio Intervention
    if ((checkboxFaceCam.get() and faceCam_OffTask_CurrentTime < OffTask_Timeout_Value) or
        (checkboxScreenCam.get() and screenCam_OffTask_CurrentTime < OffTask_Timeout_Value) or
        (checkboxSilversModel.get() and silversModel_OffTask_CurrentTime < OffTask_Timeout_Value)) and audio_intervention_playing or not audio_path:
        pygame.mixer.music.stop()
        audio_intervention_playing = False
        print("Stopped Audio")

    if not checkboxFaceCam.get() and not checkboxScreenCam.get() and not checkboxSilversModel.get() and audio_intervention_playing:
        pygame.mixer.music.stop()
        audio_intervention_playing = False
        print("Stopped Audio")


def update_data_log():
    global faceCam_OffTask_CurrentTime
    global screenCam_OffTask_CurrentTime
    global silversModel_OffTask_CurrentTime
    global OffTask_Timeout_Value
    global Model_prediction_output
    global silversModel_OnTask

    try:
        OffTask_Timeout_Value = int(entryOfftaskTimeout.get() or 10)  # Defaults to 0 if empty
    except ValueError:
        OffTask_Timeout_Value = 10  # Handle invalid input gracefully

    # Updating the FaceCam Status
    if cam1_preview.tracker.tracking_active:
        FaceCamStatusLabel.configure(text="STATUS: Active")
        SilverModelStatusLabel.configure(text="STATUS: Active")

        silver_model_input = (cam1_preview.tracker.smoothed_position[0],
                              cam1_preview.tracker.smoothed_position[1],
                              cam1_preview.tracker.smoothed_position[2],
                              cam1_preview.tracker.smoothed_angles[0],
                              cam1_preview.tracker.smoothed_angles[1],
                              cam1_preview.tracker.smoothed_angles[2])

        Model_prediction_output = silvers_model_tools.run_model(silver_model_input)
        SilverModelOutputLabel.configure(text=f"MODEL OUTPUT: {Model_prediction_output:.2f}")

        if Model_prediction_output > 0.95 or Model_prediction_output < 0.05:
            SilverModelTaskStatusLabel.configure(text="STATUS: OFF TASK", font=("Segoe UI", 14, "bold"), text_color="red")
            silversModel_OffTask_CurrentTime += 0.1
            SilverModelOffTaskTime.configure(text=f"Silvers Model Off Task time: {silversModel_OffTask_CurrentTime:.2f}")
            silversModel_OnTask = False
        else:
            SilverModelTaskStatusLabel.configure(text="STATUS: ON TASK", font=("Segoe UI", 14, "bold"),
                                                 text_color="green")
            silversModel_OnTask = True
            silversModel_OffTask_CurrentTime = 0
            SilverModelOffTaskTime.configure(text=f"Silvers Model Off Task time: {silversModel_OffTask_CurrentTime:.2f}")

    else:
        FaceCamStatusLabel.configure(text="STATUS: Not Active, Set Face Reference")
        SilverModelStatusLabel.configure(text="STATUS: Not Active, Set Face Reference")
        SilverModelOutputLabel.configure(text=f"MODEL OUTPUT: 0")

    # Updating FaceCam Task Status
    if cam1_preview.tracker.on_task and cam1_preview.tracker.tracking_active:
        FaceCamTaskStatusLabel.configure(text="TASK STATUS: ON TASK", font=("Segoe UI", 14, "bold"), text_color="green")
        faceCam_OffTask_CurrentTime = 0
        cam1_preview.tracker.offTask_currentTime = faceCam_OffTask_CurrentTime
        FaceCamOffTaskTime.configure(text=f"FaceCam Off Task time:  {faceCam_OffTask_CurrentTime:.2f}")
    else:
        FaceCamTaskStatusLabel.configure(text="TASK STATUS: OFF TASK", font=("Segoe UI", 14, "bold"), text_color="red")

        if cam1_preview.tracker.tracking_active:
            faceCam_OffTask_CurrentTime += 0.1
            cam1_preview.tracker.offTask_currentTime = faceCam_OffTask_CurrentTime
            FaceCamOffTaskTime.configure(text=f"FaceCam Off Task time:  {faceCam_OffTask_CurrentTime:.2f}")

    # Updating the FaceCam Translation Vector
    if cam1_preview.tracker.smoothed_position is not None and cam1_preview.tracker.tracking_active:
        FaceCamTVectorLabel.configure(
            text="Translation Vector: " +
                 "X: " + str(round(cam1_preview.tracker.smoothed_position[0], 2)) + " "
                                                                                    "Y: " + str(
                round(cam1_preview.tracker.smoothed_position[1], 2)) + " "
                                                                       "Z: " + str(
                round(cam1_preview.tracker.smoothed_position[2], 2)))
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
        screenCam_OffTask_CurrentTime = 0
        cam2_preview.tracker.offTask_currentTime = screenCam_OffTask_CurrentTime
        ScreenCamOffTaskTime.configure(text=f"ScreenCam Off Task time: {screenCam_OffTask_CurrentTime:.2f}")
    else:
        ScreenCamTaskStatus.configure(text="TASK STATUS: OFF TASK", font=("Segoe UI", 14, "bold"), text_color="red")

        if cam2_preview.tracker.tracking_active:
            screenCam_OffTask_CurrentTime += 0.1
            cam2_preview.tracker.offTask_currentTime = screenCam_OffTask_CurrentTime
            ScreenCamOffTaskTime.configure(text=f"ScreenCam Off Task time: {screenCam_OffTask_CurrentTime:.2f}")

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

    recorder.log_data(cam1_preview, cam2_preview, silversModel_OnTask, Model_prediction_output, silversModel_OffTask_CurrentTime, audio_intervention_playing)

    refresh_audio_intervention()

    root.after(100, update_data_log)


update_data_log()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
