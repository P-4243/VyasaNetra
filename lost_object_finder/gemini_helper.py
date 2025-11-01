
import os
from google import genai#google is a namespace package . Think of it as a large folder or container that holds many different Google-related Python tools.
#genai is a module (or sub-package) inside the google namespace..This specific module contains all the functions and classes needed to interact with Google's Generative AI models, like Gemini.
#The actual library you install (e.g., using pip install google-generativeai) provides this google.genai module.
from dotenv import load_dotenv
from navigation_helper import bbox_to_guidance
from voice_helper import speak
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# You use the dot to access the Client class that lives inside it.
#once client is created, it is a real object
# when you put parentheses after a class name, you are not just referring to the class—you are 
# giving Python a command: "Create an instance (an object) of this class for me."
def describe_objects(detected_objects, detections_with_boxes=None, frame_shape=None):
    if not detected_objects:
        speak("No objects detected.")
        return "No objects detected."

    prompt = (
        f"You are assisting a blind user. The camera sees: {', '.join(detected_objects)}. "
        "Give a short helpful description of what might be in view."
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    text_out = response.text.strip()
    speak(f"I found your {detected_objects[0]}. Here’s what I think.")
    speak(text_out)

    if detections_with_boxes and frame_shape:
        for (label, bbox) in detections_with_boxes:
            guide = bbox_to_guidance(bbox, frame_shape)
            speak(f"{label} detected. {guide['guidance_text']}")
            print(f"{label}: {guide['guidance_text']}")

    return text_out
