# voice_helper.py
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('voice', engine.getProperty('voices')[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()
