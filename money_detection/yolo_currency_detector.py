import cv2
import time
from collections import Counter
from ultralytics import YOLO
from money_detection.voice_module import speak

# Load model
import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), "MY_FINAL_CURRENCY_MODEL.pt")
model = YOLO(MODEL_PATH)


def detect_currency():
    speak("Opening camera. Hold the note steady.")

    # Try multiple indices to find an available camera
    for index in [0, 1, 2]:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            break
    else:
        cap = None
        
    if not cap.isOpened():
        speak("Camera not detected.")
        return None

    predictions = []
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls]

                # Lower threshold slightly for stability
                if conf > 0.5:
                    predictions.append(label)

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, f"{label} ({conf:.2f})",
                                (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0,255,0), 2)

        cv2.imshow("Currency Detection", frame)

        # Collect frames for 3 seconds
        if time.time() - start_time > 3:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # -------- DECISION --------

    if not predictions:
        speak("Could not detect currency.")
        return None

    most_common = Counter(predictions).most_common(1)[0][0]

    try:
        amount = int(most_common)
    except:
        speak("Detection unclear.")
        return None

    speak(f"Detected {amount} rupees.")
    return amount