import pyttsx3
import threading
import speech_recognition as sr

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
