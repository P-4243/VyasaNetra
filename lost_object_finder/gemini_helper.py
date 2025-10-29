# gemini_helper.py
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
