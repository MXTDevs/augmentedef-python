
class ScreenTracker:
    def __init__(self):
        self.can_send_request = False
        self.last_vision_llm_latency = 0
        self.tracking_active = False
        self.on_task = False
        self.last_vision_reason = ""
        self.offTask_currentTime = 0

    def start_tracking(self):
        self.tracking_active = True
        self.can_send_request = True
        self.last_vision_llm_latency = 0
        self.on_task = False
        self.last_vision_reason = ""


    def stop_tracking(self):
        self.tracking_active = False


