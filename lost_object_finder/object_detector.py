
import cv2 #While the detection itself is done by YOLO, OpenCV is used 
#here to draw the visual feedback (the rectangles and text) onto the image frame.
from ultralytics import YOLO

# Load pretrained YOLOv8 model
model = YOLO("yolov8n.pt") # 'n' stands for 'nano', which is the smallest and fastest version of the YOLOv8 models.

def detect_objects(frame):
    results = model(frame, stream=True) #for processing video streams.
    detected_items = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            name = model.names[cls] #This line translates the numeric class ID (cls) into a human-readable name.
            detected_items.append(name) #Adds the readable name of the detected object to our list of detected_items
            cv2.rectangle(frame, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                          (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (0,255,0), 2)
            cv2.putText(frame, name, (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    return frame, list(set(detected_items))
#set() first removes any duplicate detections before converting it back to a list
#