import cv2
from ultralytics import YOLO
import time
from voice_module import speak, listen


def run_object_search():
    # model = YOLO('yolov8n.pt')
    target_reached = False

    speak("What object do you want to search for?")

    TARGET_OBJECT = ""
    while not TARGET_OBJECT:
        TARGET_OBJECT = listen()

    if not TARGET_OBJECT:
        speak("Repeat clearly")
        return   # ❗ use return, NOT exit()

    SCAN_INTERVAL = 3
    last_speech_time = time.time()
    last_direction = ""

    cap = cv2.VideoCapture(2)
    model = YOLO('yolov8n.pt')
    speak(f"Searching for {TARGET_OBJECT}. Rotate slowly.")

    try:
        while cap.isOpened():
            ret, frame = cap.read()#Captures one frame
            if not ret:
                break

            h, w, _ = frame.shape#Get height & width of frame
            results = model(frame, stream=True, verbose=False)

            found_in_frame = False

            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    name = model.names[cls]

                    if TARGET_OBJECT in name or name in TARGET_OBJECT:
                        found_in_frame = True

                        x1, y1, x2, y2 = box.xyxy[0]
                        center_x = (x1 + x2) / 2#Get bounding box + center position

                        if center_x < w / 3:
                            direction = "Move left"
                            color = (0, 0, 255)
                        elif center_x > (2 * w / 3):
                            direction = "Move right"
                            color = (0, 0, 255)
                        else:
                            direction = "Straight ahead"
                            color = (0, 255, 0)

                        box_width_ratio = (x2 - x1) / w

                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                        cv2.putText(frame, direction, (int(x1), int(y1)-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                        current_time = time.time()

                        if current_time - last_speech_time > 1.5:

                            if direction == "Straight ahead" and box_width_ratio > 0.4:
                                speak(f"Stop! The {TARGET_OBJECT} is right in front of you.")
                                target_reached = True
                                break

                            if direction != last_direction:
                                speak(direction)
                                last_direction = direction

                            last_speech_time = current_time

                if target_reached:
                    break

            if target_reached:
                break

            if not found_in_frame:
                current_time = time.time()
                if current_time - last_speech_time > SCAN_INTERVAL:
                    speak("Keep scanning.")
                    last_speech_time = current_time

            cv2.imshow("Object Finder", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print("Error:", e)

    finally:
        cap.release()
        cv2.destroyAllWindows()