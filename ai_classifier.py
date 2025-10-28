from google import genai
from datetime import datetime

# ✅ Initialize Gemini client
client = genai.Client(api_key="")

def interpret_medicine_info(ocr_text):
    """
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

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"[AI Error] {e}"

