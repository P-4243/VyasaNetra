import pyttsx3
import speech_recognition as sr

def speak(text):
    """Speaks the given text aloud and prints it to console."""
    print("\nAssistant:", text)
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait() #Blocks further code execution until all the queued speech is finished
        engine.stop() 
    except Exception as e:
        print(f"[Speech Error] {e}")

def listen():
    r = sr.Recognizer()
    r.energy_threshold = 300  # 🔥 helps in noisy rooms
    r.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("Listening...")

        r.adjust_for_ambient_noise(source, duration=1)  # 🔥 increase this
        # r.pause_threshold = 1.2  # wait for user to finish speaking

        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=4)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything.")
            return ""

    try:
        text = r.recognize_google(audio, language="en-US")  # 🔥 change this
        print(f"You said: {text}")
        return text.lower().strip()

    except sr.UnknownValueError:
        speak("Sorry, I couldn’t understand that clearly.")
    except sr.RequestError:
        speak("Network error. Please check your internet.")

    return ""
