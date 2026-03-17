import cv2
from ultralytics import YOLO
import pyttsx3
import time

# --- INITIALIZATION ---
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Speed of speech

def speak(text):
    print(f"ASSISTANT: {text}")
    engine.say(text)
    engine.runAndWait()

# Load the fastest model
model = YOLO('yolov8n.pt') 

# --- CONFIGURATION ---
TARGET_OBJECT = input("Enter object to find (e.g., chair, bottle, cell phone): ").lower()
SCAN_INTERVAL = 3  # Seconds between "Keep scanning" prompts
last_speech_time = time.time()

cap = cv2.VideoCapture(0)
speak(f"System active. Searching for {TARGET_OBJECT}. Please rotate your phone slowly.")

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        h, w, _ = frame.shape
        results = model(frame, stream=True, verbose=False)
        
        found_in_frame = False
        
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                name = model.names[cls]
                
                if name == TARGET_OBJECT:
                    found_in_frame = True
                    # 1. Get Coordinates
                    x1, y1, x2, y2 = box.xyxy[0]
                    center_x = (x1 + x2) / 2
                    
                    # 2. RADAR/DIRECTION LOGIC
                    # Divide screen into 3 zones
                    if center_x < w / 3:
                        direction = "Move left"
                        color = (0, 0, 255) # Red for "not centered"
                    elif center_x > (2 * w / 3):
                        direction = "Move right"
                        color = (0, 0, 255)
                    else:
                        direction = "Straight ahead"
                        color = (0, 255, 0) # Green for "Centered"

                    # 3. PROXIMITY LOGIC (Distance estimation)
                    box_width_ratio = (x2 - x1) / w
                    
                    # Draw for Mam to see
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    cv2.putText(frame, f"{direction}", (int(x1), int(y1)-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                    # 4. FEEDBACK & STOPPING CONDITION
                    current_time = time.time()
                    if current_time - last_speech_time > 1.5: # Voice guidance every 1.5s
                        if direction == "Straight ahead" and box_width_ratio > 0.4:
                            speak(f"Stop! The {TARGET_OBJECT} is right in front of you.")
                            cap.release()
                            cv2.destroyAllWindows()
                            exit()
                        else:
                            speak(direction)
                        last_speech_time = current_time

        # 5. SCANNING HELPER (If object is not in sight)
        if not found_in_frame:
            current_time = time.time()
            if current_time - last_speech_time > SCAN_INTERVAL:
                speak("Object not found. Continue scanning the room slowly.")
                last_speech_time = current_time

        cv2.imshow("Third Eye - Object Finder", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

except Exception as e:
    print(f"Error: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()