from tkinter import *
from voice_module import speak, listen, get_intent
from camera_module import open_camera
from ocr_module import extract_text_from_frame, analyze_text
import pytesseract

def capture_and_analyze(result_box):
    frame = open_camera()
    if frame is None:
        return
    speak("Image captured. Processing...")
    text = extract_text_from_frame(frame, pytesseract)
    analyze_text(text, result_box)

def start_voice_command(result_box):
    query = listen()
    intent = get_intent(query)
    if intent == "medicine_info":
        capture_and_analyze(result_box)
    else:
        speak("Sorry, I can only help with medicine details right now.")

def start_gui():
    root = Tk()
    root.title("AI Medicine Identifier - Voice + Camera")
    root.geometry("600x400")
    root.config(bg="black")

    Label(root, text="AI Medicine Identifier", fg="white", bg="black",
          font=("Arial", 20, "bold")).pack(pady=20)

    result_box = Text(root, wrap=WORD, width=60, height=10, font=("Arial", 12))
    result_box.pack(pady=10)

    Button(root, text="🎙 Speak Command", font=("Arial", 14, "bold"),
           command=lambda: start_voice_command(result_box),
           bg="blue", fg="white", padx=20, pady=10).pack(pady=10)

    Button(root, text="📷 Open Camera", font=("Arial", 14, "bold"),
           command=lambda: capture_and_analyze(result_box),
           bg="green", fg="white", padx=20, pady=10).pack(pady=10)

    Label(root, text="Press SPACE to capture | Q to quit camera",
          fg="lightgray", bg="black", font=("Arial", 10)).pack(pady=5)

    root.mainloop()
