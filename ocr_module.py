from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
# ✅ Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_image(image_path):
    """
    Uses Gemini 2.5 Flash to perform OCR and understand the text
    directly from the uploaded image.
    """
    # Read the image file
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()

    prompt = """
    You are an AI OCR and medicine-label reader.
    Carefully extract all readable text from the image,
    especially the medicine name, manufacturing (MFG) date,
    expiry (EXP), and usage details.
    Return all extracted text clearly, followed by a summary.
    """

    # ✅ Correct structure for google-genai
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            {"role": "user", "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": image_bytes}}
            ]}
        ]
    )

    return response.text.strip()
