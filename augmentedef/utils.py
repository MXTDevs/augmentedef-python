from pygrabber.dshow_graph import FilterGraph
from scipy.spatial.transform import Rotation as R
import numpy as np

import platform

# Try to use pygrabber for camera names on Windows
device_names = []
if platform.system() == "Windows":
    try:
        graph = FilterGraph()
        device_names = graph.get_input_devices()  # Returns a list of device names
        string_device_names = ""
        for i in device_names:
            string_device_names = string_device_names + " , " + i
        print("Known devices: " + string_device_names)
    except Exception as e:
        print("Error retrieving camera names using pygrabber:", e)


def rotation_vector_to_euler(rvec):
    """Convert rotation vector to Euler angles (pitch, yaw, roll)"""
    rotation = R.from_rotvec(rvec.flatten()).as_euler('ZYX', degrees=True)
    return rotation[2], rotation[1], rotation[0]


def smooth_values(buffer, new_values, count):
    """Apply moving average smoothing over the frames seen so far"""
    buffer[count % 5] = new_values
    effective_count = min(count + 1, 5)
    return np.mean(buffer[:effective_count], axis=0)
