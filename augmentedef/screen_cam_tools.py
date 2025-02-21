import cv2
from openai import OpenAI
from dotenv import load_dotenv

import base64
import os
import time
import concurrent.futures

from augmentedef import screen_tracker

# Load environment variables from the .env file
load_dotenv()

project_api_key = os.getenv("OPENAI_API_KEY")

# Set up OpenAI client
client = OpenAI(api_key=project_api_key)


def process_frame(frame, tracker: screen_tracker.ScreenTracker()):
    # If we cannot send a request because a previous request is still not completed
    # we return
    if tracker.can_send_request is False or tracker.tracking_active is False:
        return

    tracker.can_send_request = False

    start_time = time.time()

    # Capture the current frame image and save it
    base64_image = capture_image(frame)

    # Analyzing the image
    print("Analyzing image...")
    analysis = analyze_image(base64_image)
    verdict, reason = parse_response(analysis)

    print(f"\nProductivity Analysis:")
    print(f"Status: {verdict}")
    print(f"Reason: {reason}")

    if "ON TASK" in str(verdict):
        tracker.on_task = True
    else:
        tracker.on_task = False

    end_time = time.time()

    tracker.last_vision_reason = reason
    tracker.last_vision_llm_latency = end_time - start_time

    time.sleep(0)

    print("Request Took: ", str(tracker.last_vision_llm_latency))
    tracker.can_send_request = True


def capture_image(frame):
    current_frame = frame
    cv2.imwrite("captured_image.jpg", current_frame)
    print("Captured Image and Saved")

    # Convert image to RGB and encode as JPEG
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    _, buffer = cv2.imencode('.jpg', rgb_image)
    return base64.b64encode(buffer).decode('utf-8')


def analyze_image(base64_image, max_timeout=10, max_retries=3):
    analysis_prompt = """SYSTEM ROLE: Workplace Productivity Analyst. Analyze strictly based on visible evidence.

        TASK: Determine if user is actively engaged with computer based on this image taken from the Point of View of the user. Consider:
        1. Visible items
        2. Hand position (keyboard/mouse vs idle)
        3. Screen activity (screen content)
        4. Competing distractions in frame

        DECISION CRITERIA:
        ✅ ON TASK if:
        - Computer screen, keyboard or mouse are visible
        - Hands interacting with input devices
        - Active screen content
        - Work related content
        - No competing focus elements

        ❌ OFF TASK if:
        - No computer screen visible, no keyboard or mouse visible
        - Main items in the image are not work related
        - Screen content is not work related
        - Large distraction items
        - Social media content such as Facebook or Youtube
        - Screen locked/blank or pure black

        RESPONSE FORMAT: STRICTLY FOLLOW:
        VERDICT: [ON TASK/OFF TASK]
        REASON: [1-2 sentence explanation based on visual evidence]"""

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(client.chat.completions.create,
                                         model="gpt-4o-mini",
                                         messages=[
                                             {
                                                 "role": "user",
                                                 "content": [
                                                     {"type": "text", "text": analysis_prompt},
                                                     {
                                                         "type": "image_url",
                                                         "image_url": {
                                                             "url": f"data:image/jpeg;base64,{base64_image}",
                                                             "detail": "low",
                                                         }
                                                     },
                                                 ],
                                             }
                                         ],
                                         max_tokens=300
                                         )

                response = future.result(timeout=max_timeout)  # Set timeout here
                return response.choices[0].message.content

        except concurrent.futures.TimeoutError:
            print(f"Request timed out (Attempt {attempt}/{max_retries}), retrying...")
        except Exception as e:
            print(f"An error occurred: {e}")
            break  # Break the loop on unexpected errors

    print("Failed to analyze image after multiple attempts.")
    return "VERDICT: OFF TASK\nREASON: Unable to process image due to timeout."




def parse_response(response):
    verdict = None
    reason = ""

    if "VERDICT:" in response:
        verdict_line = response.split("VERDICT:")[1].split("\n")[0].strip()
        verdict = verdict_line if verdict_line in ["ON TASK", "OFF TASK"] else None

    if "REASON:" in response:
        reason = response.split("REASON:")[1].strip()

    return verdict, reason
