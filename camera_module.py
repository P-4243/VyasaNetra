import cv2
import tempfile
import os
from voice_module import speak
from ocr_module import extract_text_from_image
from ai_classifier import interpret_medicine_info

def open_camera():
    """Opens webcam, captures an image, and returns the frame."""
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
        if key == 32:  # SPACE key
            captured_frame = frame
            speak("Image captured successfully.")
            break
        elif key == ord('q'):
            speak("Camera closed.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return captured_frame


def process_camera_image():
    """Captures image → extracts text → gets AI interpretation."""
    frame = open_camera()
    if frame is None:
        speak("No image captured.")
        return

    # Save temporarily for OCR
    temp_path = os.path.join(tempfile.gettempdir(), "captured_image.jpg")
    cv2.imwrite(temp_path, frame)

    # Step 1: OCR Extraction
    text = extract_text_from_image(temp_path)
    if not text.strip():
        speak("No text detected in image.")
        return

    speak("Text extracted successfully.")
    print("\n🔍 Extracted Text:\n", text)

    # Step 2: AI Classification (Gemini)
    result = interpret_medicine_info(text)
    print("\n🤖 Gemini AI Output:\n", result)
    speak(result)


if __name__ == "__main__":
    process_camera_image()
