from google import genai # Imports Google's Generative AI library
from datetime import datetime #  get the current date for expiry comparison
from dotenv import load_dotenv #function to load environment variables from a .env file
import os #interact directly with the operating system — like reading files
load_dotenv() #Loads environment variables from .env file into the system

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))#Creates a Gemini AI client using the API key


def interpret_medicine_info(ocr_text):
    """
    the 3 "- it’s a docstring, i.e. documentation for the function.
    Sends OCR text to Gemini 2.5 for intelligent interpretation.
    Detects MFG, EXP, and checks expiry validity.

    """
    prompt = f"""
    You are an AI that analyzes medicine labels.
    OCR text:
    \"\"\"{ocr_text}\"\"\"

    Tasks:
    1. Identify medicine name (if present)
    2. Detect manufacturing (MFG) and expiry (EXP) dates
    3. Compare expiry with today's date ({datetime.now().strftime("%d-%m-%Y")})
    4. Summarize result in plain language, e.g.:
       "This is Crocin 500 mg. MFG: Jan 2023, EXP: Dec 2025. The medicine is valid."
    """
    #So if today is 29th October 2025, then datetime.now().strftime("%d-%m-%Y") → "29-10-2025"
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()#Returns the AI's response text with whitespace removed
    except Exception as e:
        return f"[AI Error] {e}" #f"..." means formatted string literal.It lets you insert variables or expressions directly inside {}

