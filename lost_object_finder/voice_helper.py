# voice_helper.py
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('voice', engine.getProperty('voices')[1].id)
#list of all the different voice profiles it can find on your computer
#This list is just like any other Python list. It might look something like this conceptually: [ <Voice object for David>, <Voice object for Zira>, <Voice object for Mark> ]
def speak(text):
    engine.say(text)
    engine.runAndWait()
