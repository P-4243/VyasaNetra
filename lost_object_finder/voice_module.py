# voice_module.py
import speech_recognition as sr
from voice_helper import speak

def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Please say what you want to find.")
        print("Listening...")
        audio = r.listen(source, timeout=5, phrase_time_limit=5)

    try:
        command = r.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service not available right now.")
        return ""
