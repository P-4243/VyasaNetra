import pyttsx3
import speech_recognition as sr
import time

# ------------------ INIT ONCE ------------------
# engine = pyttsx3.init()
# engine.setProperty('rate', 170)

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True


# ------------------ SPEAK ------------------
def speak(text):
    print("\nAssistant:", text)
    try:
        engine = pyttsx3.init()   # 🔥 re-init every time (fixes freeze)
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        time.sleep(0.3)
    except Exception as e:
        print(f"[Speech Error] {e}")


# ------------------ LISTEN ------------------
def listen():
    time.sleep(0.8)  # Brief pause before listening
    with sr.Microphone() as source:
        print("Listening...")

        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=4)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything.")
            return ""

    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"You said: {text}")
        return text.lower().strip()

    except sr.UnknownValueError:
        speak("Sorry, I couldn’t understand that clearly.")
    except sr.RequestError:
        speak("Network error. Please check your internet.")

    return ""