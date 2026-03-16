import cv2
from ultralytics import YOLO
import pyttsx3
import time
import winsound  # For the "Radar" pings

# --- INITIALIZATION ---
engine = pyttsx3.init()
engine.setProperty('rate', 200)

def speak(text):
    print(f"AUDIO FEEDBACK: {text}") # Still printing for Mam to see
    engine.say(text)
    engine.runAndWait()

def play_radar_ping(freq):
    # Short beep to act as a distance/alignment sensor
    winsound.Beep(freq, 100)

# Load the fast YOLOv8 Nano model
model = YOLO('yolov8n.pt') 

# --- CONFIGURATION ---
TARGET_OBJECT = input("Enter object to find: ").lower()
SCAN_INTERVAL = 4.0  # Time between "Keep scanning" prompts
last_speech_time = time.time()

cap = cv2.VideoCapture(0)
speak(f"System active. Searching for {TARGET_OBJECT}. Please rotate slowly.")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        h, w, _ = frame.shape
        results = model(frame, stream=True, verbose=False)
        found_in_frame = False
        
        for r in results:
            for box in r.boxes:
                name = model.names[int(box.cls[0])]
                
                if name == TARGET_OBJECT:
                    found_in_frame = True
                    x1, y1, x2, y2 = box.xyxy[0]
                    center_x = (x1 + x2) / 2
                    box_width_ratio = (x2 - x1) / w
                    
                    current_time = time.time()
                    
                    # 1. RADAR / DIRECTIONAL GUIDANCE
                    if center_x < w / 3:
                        if current_time - last_speech_time > 1.2:
                            speak("Move left")
                            last_speech_time = current_time
                    elif center_x > (2 * w / 3):
                        if current_time - last_speech_time > 1.2:
                            speak("Move right")
                            last_speech_time = current_time
                    else:
                        # 2. THE "LOCK-ON" PING (Object is Centered)
                        play_radar_ping(1200) # High pitch beep
                        
                        # 3. STOPPING CONDITION / PROXIMITY
                        if box_width_ratio > 0.45:
                            speak(f"Stop! {TARGET_OBJECT} is right here.")
                            cap.release()
                            cv2.destroyAllWindows()
                            exit()
                        elif current_time - last_speech_time > 1.5:
                            speak("Straight ahead")
                            last_speech_time = current_time

        # 4. SCANNING HELPER (If object is lost)
        if not found_in_frame:
            current_time = time.time()
            if current_time - last_speech_time > SCAN_INTERVAL:
                speak("Object not seen. Continue scanning right.")
                last_speech_time = current_time

        # Visual bounding box for the teacher's benefit
        cv2.imshow("Third Eye Assistant", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

finally:
    cap.release()
    cv2.destroyAllWindows()