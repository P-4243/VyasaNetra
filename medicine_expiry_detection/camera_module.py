import cv2
import tempfile
import os
import time

from voice_module import speak
from ocr_module import extract_text_from_image
from ai_classifier import interpret_medicine_info


# ------------------ ALIGNMENT CHECK ------------------
def is_medicine_aligned(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blur, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return False

    largest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest)

    if area < 5000:
        return False

    x, y, w, h = cv2.boundingRect(largest)

    frame_h, frame_w = frame.shape[:2]

    center_x = x + w / 2
    center_y = y + h / 2

    # Check center alignment
    if abs(center_x - frame_w / 2) < frame_w * 0.2 and abs(center_y - frame_h / 2) < frame_h * 0.2:
        return True

    return False


# ------------------ CAMERA ------------------
def open_camera():
    speak("Opening camera. Please hold the medicine label in front.")

    cap = cv2.VideoCapture(2)

    if not cap.isOpened():
        speak("Camera not detected.")
        return None

    cv2.namedWindow("Camera View", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera View", 640, 480)

    captured_frame = None
    aligned_frames = 0
    last_feedback_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display_frame = frame.copy()
        h, w, _ = display_frame.shape

        # ---------------- ALIGNMENT CHECK ----------------
        if is_medicine_aligned(frame):
            aligned_frames += 1

            cv2.putText(display_frame, "Hold steady...",
                        (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        else:
            aligned_frames = 0

            if time.time() - last_feedback_time > 3:
                speak("Please align the medicine properly in the center")
                last_feedback_time = time.time()

            cv2.putText(display_frame, "Align properly",
                        (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # ---------------- AUTO CAPTURE ----------------
        if aligned_frames > 15:
            speak("Perfect. Capturing image.")
            captured_frame = frame
            break

        cv2.imshow("Camera View", display_frame)

        # Quit manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            speak("Camera closed.")
            break

    cap.release()
    cv2.destroyAllWindows()

    return captured_frame


# ------------------ PROCESS ------------------
def process_camera_image():
    frame = open_camera()

    if frame is None:
        speak("No image captured.")
        return

    temp_path = os.path.join(tempfile.gettempdir(), "captured_image.jpg")
    cv2.imwrite(temp_path, frame)

    text = extract_text_from_image(temp_path)

    if not text.strip():
        speak("No text detected in image.")
        return

    speak("Text extracted successfully.")
    print("\n🔍 Extracted Text:\n", text)

    result = interpret_medicine_info(text)

    print("\n🤖 AI Output:\n", result)
    speak(result)


# ------------------ RUN ------------------
if __name__ == "__main__":
    process_camera_image()