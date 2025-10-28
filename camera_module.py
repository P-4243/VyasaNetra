import cv2
from voice_module import speak

def open_camera():
    speak("Opening camera. Please hold the medicine label in front.")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Camera not detected.")
        return None
    cv2.namedWindow("Camera View", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera View", 640, 480)
    captured_frame = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        display_frame = frame.copy()
        h, w, _ = display_frame.shape
        cv2.putText(display_frame, "Press SPACE to capture | Q to quit",
                    (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Camera View", display_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 32:
            captured_frame = frame
            break
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return captured_frame
