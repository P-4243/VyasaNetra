import cv2
from ultralytics import YOLO
import time
from voice_module import speak, listen

def run_object_search():
    # --- CONFIGURATION ---
    KNOWN_WIDTH = 15.0     # Width of target object in cm (e.g., a laptop or large bottle)
    FOCAL_LENGTH = 600.0   # Calibrated focal length of your camera
    CM_PER_STEP = 60.0     # Average step length in cm
    
    cap = cv2.VideoCapture(2)
    model = YOLO(r"C:\Users\sophi\OneDrive\Desktop\FALTU🗑️\👻Project\VyasNetra App\object_search\best.pt")
    
    speak("What object do you want to search for?")
    TARGET_OBJECT = ""
    while not TARGET_OBJECT:
        TARGET_OBJECT = listen()

    last_speech_time = time.time()
    last_instruction = ""

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            h, w, _ = frame.shape
            cam_center_x = w / 2
            results = model(frame, stream=True, verbose=False)
            found_in_frame = False

            for r in results:
                for box in r.boxes:
                    name = model.names[int(box.cls[0])]
                    if TARGET_OBJECT.lower() in name.lower():
                        found_in_frame = True
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        
                        # 1. Calculate Depth (Distance from camera to object)
                        pixel_width = x2 - x1
                        distance_cm = (KNOWN_WIDTH * FOCAL_LENGTH) / pixel_width
                        
                        # 2. Calculate Horizontal Offset (How far off-center)
                        obj_center_x = (x1 + x2) / 2
                        # Offset in pixels relative to center
                        offset_pixels = obj_center_x - cam_center_x
                        
                        # Convert pixel offset to real-world cm 
                        # (Formula: offset_cm = (offset_pix * distance_cm) / FOCAL_LENGTH)
                        offset_cm = (offset_pixels * distance_cm) / FOCAL_LENGTH
                        
                        # 3. Convert to Steps
                        horizontal_steps = abs(round(offset_cm / CM_PER_STEP))
                        forward_steps = round(distance_cm / CM_PER_STEP)

                        # 4. Determine Instruction
                        if offset_cm < -20: # Object is significantly to the left
                            direction = f"{max(1, horizontal_steps)} steps left"
                        elif offset_cm > 20: # Object is significantly to the right
                            direction = f"{max(1, horizontal_steps)} steps right"
                        else:
                            direction = "straight ahead"

                        # 5. Speech Logic
                        current_time = time.time()
                        if current_time - last_speech_time > 2.5: # Don't spam instructions
                            
                            if distance_cm < 40: # Within reaching distance
                                speak(f"Stop. The {name} is right in front of you.")
                                return
                            
                            if direction == "straight ahead":
                                instruction = f"{forward_steps} steps forward straight"
                            else:
                                instruction = direction

                            if instruction != last_instruction:
                                speak(instruction)
                                last_instruction = instruction
                            
                            last_speech_time = current_time

                        # Visuals for debugging
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        cv2.putText(frame, f"Dist: {int(distance_cm)}cm | Off: {int(offset_cm)}cm", 
                                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow("Object Finder", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

    finally:
        cap.release()
        cv2.destroyAllWindows()