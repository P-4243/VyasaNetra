import pyttsx3
import speech_recognition as sr
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Assistant:", text)
    def run_speech():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run_speech, daemon=True).start()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening now. You can say — Tell me about this medicine.")
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.8)
        audio = r.listen(source, timeout=6, phrase_time_limit=6)
    try:
        text = r.recognize_google(audio, language="en-IN")
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
    if best_match_value > 0.3:
        return "medicine_info"
    return None
