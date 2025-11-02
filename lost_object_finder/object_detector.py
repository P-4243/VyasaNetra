import cv2
from ultralytics import YOLO

# Load pretrained YOLOv8 model
model = YOLO("yolov8n.pt")  # 'n' = nano (lightweight, fast)

def detect_objects(frame):
    """
    Detects objects using YOLO and returns:
    - frame with bounding boxes drawn
    - detected_items: list of object names
    - boxes_dict: dictionary mapping object name -> list of bounding boxes
    """
    results = model(frame, stream=True)
    detected_items = []
    boxes_dict = {}

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            name = model.names[cls]

            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detected_items.append(name)
            boxes_dict.setdefault(name, []).append((x1, y1, x2, y2))

            # Draw rectangle + label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return frame, list(set(detected_items)), boxes_dict
