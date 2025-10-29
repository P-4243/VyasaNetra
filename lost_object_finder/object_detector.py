# object_detector.py
import cv2
from ultralytics import YOLO

# Load pretrained YOLOv8 model
model = YOLO("yolov8n.pt")  # small model for fast detection

def detect_objects(frame):
    results = model(frame, stream=True)
    detected_items = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            name = model.names[cls]
            detected_items.append(name)
            cv2.rectangle(frame, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                          (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (0,255,0), 2)
            cv2.putText(frame, name, (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    return frame, list(set(detected_items))
