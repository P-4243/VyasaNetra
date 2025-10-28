import cv2
import pytesseract
import pyttsx3
import re
from tkinter import *
from datetime import datetime
from dateutil.parser import parse as dateparse
import speech_recognition as sr
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ------------- SPEECH ENGINE ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 170)

import threading

def speak(text):
    print("Assistant:", text)
    def run_speech():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run_speech, daemon=True).start()


# ------------- LISTEN + NLP MATCH ----------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening now. You can say — Tell me about this medicine.")
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.8)  # improves accuracy
        audio = r.listen(source, timeout=6, phrase_time_limit=6)

    try:
        text = r.recognize_google(audio, language="en-IN")  # Indian accent support
        print(f"You said: {text}")
        return text.lower().strip()
    except sr.WaitTimeoutError:
        speak("I didn’t hear anything.")
    except sr.UnknownValueError:
        speak("Sorry, I couldn’t understand that.")
    except sr.RequestError:
        speak("Network error. Please check your connection.")
    return ""

intents = {
    "medicine_info": [
        "tell me about this medicine",
        "check expiry date",
        "read my medicine",
        "medicine information",
        "verify my tablet",
        "identify this medicine"
    ]
}

def get_intent(user_text):
    if not user_text:
        return None
    texts = [user_text] + [p for intent in intents.values() for p in intent]
    vec = CountVectorizer().fit_transform(texts)
    similarity = cosine_similarity(vec[0:1], vec[1:]).flatten()
    best_match_index = similarity.argmax()
    best_match_value = similarity[best_match_index]

    print(f"Intent similarity: {best_match_value:.2f}")
    if best_match_value > 0.3:  # slightly relaxed threshold
        return "medicine_info"
    return None

# ------------- OCR + EXPIRY EXTRACTION ----------------
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

    text = extract_text_from_image(frame)
    print("Detected text:\n", text)

    # Extract all date-like patterns (dd-mm-yyyy / dd/mm/yyyy)
    date_matches = re.findall(r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b', text)
    parsed_dates = []

    for d in date_matches:
        for fmt in ("%d-%m-%Y", "%d/%m/%Y", "%d-%m-%y", "%d/%m/%y"):
            try:
                parsed_dates.append(datetime.strptime(d, fmt))
                break
            except:
                continue

    result_box.delete(1.0, END)
    result_box.insert(END, f"Detected text:\n{text}\n")

    if len(parsed_dates) >= 2:
        parsed_dates.sort()
        mfg_date = parsed_dates[0].strftime("%d-%m-%Y")
        exp_date = parsed_dates[-1].strftime("%d-%m-%Y")

        result_box.insert(END, f"\nManufacturing Date: {mfg_date}")
        result_box.insert(END, f"\nExpiry Date: {exp_date}")

        if datetime.now() > parsed_dates[-1]:
            status = "⚠️ This medicine has expired."
        else:
            status = "✅ This medicine is valid."
        result_box.insert(END, f"\n{status}")

        speak(f"I found two dates. The medicine was manufactured on {mfg_date} and expires on {exp_date}. {status}")
    elif len(parsed_dates) == 1:
        single_date = parsed_dates[0].strftime("%d-%m-%Y")
        result_box.insert(END, f"\nOnly one date found: {single_date}")
        speak(f"I found one date: {single_date}. I couldn’t tell if it's manufacturing or expiry.")
    else:
        result_box.insert(END, "\nNo valid dates found.")
        speak("No valid date detected. Please try again.")
# ------------- VOICE TRIGGER ----------------
def start_voice_command():
    query = listen()
    intent = get_intent(query)
    if intent == "medicine_info":
        capture_and_analyze()
    else:
        speak("Sorry, I can only help with medicine details right now.")


# ------------- GUI ----------------

root = Tk()
root.title("AI Medicine Identifier - Voice + Camera")
root.geometry("600x400")
root.config(bg="black")

Label(root, text="AI Medicine Identifier", fg="white", bg="black",
      font=("Arial", 20, "bold")).pack(pady=20)

Button(root, text="🎙 Speak Command", font=("Arial", 14, "bold"),
       command=start_voice_command, bg="blue", fg="white", padx=20, pady=10).pack(pady=10)

Button(root, text="📷 Open Camera", font=("Arial", 14, "bold"),
       command=capture_and_analyze, bg="green", fg="white", padx=20, pady=10).pack(pady=10)

result_box = Text(root, wrap=WORD, width=60, height=10, font=("Arial", 12))
result_box.pack(pady=10)

Label(root, text="Press SPACE to capture | Q to quit camera",
      fg="lightgray", bg="black", font=("Arial", 10)).pack(pady=5)

root.mainloop()
