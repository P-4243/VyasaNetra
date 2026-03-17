import pyttsx3
import speech_recognition as sr

def speak(text):
    """Speaks the given text aloud and prints it to console."""
    print(f"\n[Assistant]: {text}")
    try:
        # Initialize inside the function to avoid 'runloop already started' errors
        engine = pyttsx3.init()
        engine.setProperty('rate', 185) # Optimal speed for clear guidance
        engine.say(text)
        engine.runAndWait() 
        engine.stop() 
    except Exception as e:
        print(f"[Speech Error] {e}")

def listen():
    """Listens to microphone input and returns recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # Reduced ambient noise duration to make it feel more responsive
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening for object name...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
            text = r.recognize_google(audio, language="en-IN")
            print(f"User said: {text}")
            return text.lower().strip()
        except Exception:
            # If it fails, returning empty string lets main.py handle the default
            return ""