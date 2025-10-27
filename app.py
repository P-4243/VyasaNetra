import cv2
import pytesseract
import pyttsx3
import re
from tkinter import *
from datetime import datetime
from dateutil.parser import parse as dateparse

# ------------- SPEECH ENGINE ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # speech speed

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ------------- OCR + EXPIRY EXTRACTOR ----------------
def extract_text_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

DATE_PATTERNS = [
    r'(?:exp|expiry|exp\.?|EXP|EXPIRY|best before)[:\s]*([0-9]{1,2}[/\-\.][0-9]{2,4})',
    r'(?:exp|expiry|EXP)[\s:]*([0-9]{2}[/\-][0-9]{4})',
    r'\b([0-9]{2}[/\-][0-9]{2}[/\-][0-9]{2,4})\b',
    r'\b([0-9]{1,2}\s?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s?[0-9]{2,4})\b',
    r'\b(0[1-9]|1[0-2])\s?/\s?([0-9]{2,4})\b',
]

def find_expiry(text):
    for pat in DATE_PATTERNS:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            candidate = m.group(1)
            try:
                dt = dateparse(candidate, fuzzy=True, dayfirst=False)
                return dt.date().isoformat()
            except Exception:
                continue
    return None

# ------------- CAMERA CAPTURE + ANALYZE ----------------
def capture_and_analyze():
    speak("Opening camera. Please hold the medicine label in front.")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        speak("Camera not detected.")
        return

    cv2.namedWindow("Camera View", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Camera View", 640, 480)

    captured = False
    frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Show a visual guide
        display_frame = frame.copy()
        h, w, _ = display_frame.shape
        cv2.putText(display_frame, "Press SPACE to capture | Q to quit",
                    (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Camera View", display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # SPACEBAR
            captured = True
            break
        elif key == ord('q'):
            break

    if not captured:
        speak("No image captured.")
        cap.release()
        cv2.destroyAllWindows()
        return

    speak("Image captured. Processing...")
    cap.release()
    cv2.destroyAllWindows()

    # Perform OCR and expiry extraction
    text = extract_text_from_image(frame)
    expiry = find_expiry(text)

    result = f"Detected text: {text[:100]}..."  # show first 100 chars
    result_box.delete(1.0, END)
    result_box.insert(END, result + f"\nExpiry: {expiry or 'Not found'}")

    if expiry:
        speak(f"The expiry date found is {expiry}.")
    else:
        speak("No expiry date detected. Please try again.")

# ------------- GUI ----------------
root = Tk()
root.title("AI Medicine Identifier - Camera Mode")
root.geometry("600x400")
root.config(bg="black")

Label(root, text="AI Medicine Identifier", fg="white", bg="black",
      font=("Arial", 20, "bold")).pack(pady=20)

Button(root, text="Open Camera", font=("Arial", 14, "bold"),
       command=capture_and_analyze, bg="green", fg="white", padx=20, pady=10).pack(pady=10)

result_box = Text(root, wrap=WORD, width=60, height=10, font=("Arial", 12))
result_box.pack(pady=10)

Label(root, text="Press SPACE to capture | Q to quit camera",
      fg="lightgray", bg="black", font=("Arial", 10)).pack(pady=5)

root.mainloop()
