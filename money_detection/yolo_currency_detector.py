import cv2
import time
from collections import Counter
from ultralytics import YOLO
from voice_module import speak

# Load your trained model
model = YOLO("money_detection/best.pt")


def detect_currency():

    speak("Opening camera. Show the note clearly.")

    cap = cv2.VideoCapture(2)

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

                # Only consider confident predictions
                if conf > 0.6:
                    predictions.append(label)

                    # Draw box
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                    cv2.putText(frame, f"{label} ({conf:.2f})",
                                (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0,255,0), 2)

        cv2.imshow("Currency Detection", frame)

        # Collect for ~3 seconds
        if time.time() - start_time > 3:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # ------------------ DECISION ------------------

    if not predictions:
        speak("Could not detect currency.")
        return None

    # Majority voting
    most_common = Counter(predictions).most_common(1)[0][0]

    # Convert label → integer
    try:
        amount = int(most_common)
    except:
        speak("Detected label is unclear.")
        return None

    speak(f"Detected {amount} rupees.")
    return amount