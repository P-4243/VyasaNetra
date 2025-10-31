
import os
from google import genai#google is a namespace package . Think of it as a large folder or container that holds many different Google-related Python tools.
#genai is a module (or sub-package) inside the google namespace..This specific module contains all the functions and classes needed to interact with Google's Generative AI models, like Gemini.
#The actual library you install (e.g., using pip install google-generativeai) provides this google.genai module.
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# You use the dot to access the Client class that lives inside it.
#once client is created, it is a real object
# when you put parentheses after a class name, you are not just referring to the class—you are 
# giving Python a command: "Create an instance (an object) of this class for me."
def describe_objects(detected_objects):
    """
    Send detected object list to Gemini and ask for a natural-language description.
    """
    prompt = f"You are assisting a blind user. The camera sees: {', '.join(detected_objects)}. " \
             f"Give a short helpful description of where each item might be located or if it matches a 'wallet' or 'keys'."
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()
