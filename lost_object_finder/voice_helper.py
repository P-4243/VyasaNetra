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

def listen_for_command():
    """Listens to microphone input and returns recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #speak("Listening now. You can say — Tell me about this medicine.")
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
