import cv2
import re
from datetime import datetime
from dateutil.parser import parse as dateparse
from voice_module import speak

import pytesseract


def extract_text_from_image(image_path):
    # Read image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Optional: Apply thresholding to enhance text visibility
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Extract text using Tesseract OCR
    text = pytesseract.image_to_string(thresh)
    return text.strip()

def extract_text_from_frame(frame, pytesseract):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

def find_dates(text):
    DATE_PATTERNS = [
        r'(?:exp|expiry|exp\.?|best before)[:\s]*([0-9]{1,2}[/\-\.][0-9]{2,4})',
        r'(?:exp|expiry)[\s:]*([0-9]{2}[/\-][0-9]{4})',
        r'\b([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})\b',
        r'\b([0-9]{1,2}\s?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s?[0-9]{2,4})\b',
    ]
    found = []
    for pat in DATE_PATTERNS:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            candidate = m.group(1)
            try:
                dt = dateparse(candidate, fuzzy=True, dayfirst=False)
                found.append(dt)
            except Exception:
                continue
    return found

def analyze_text(text, result_box):
    from datetime import datetime
    result_box.delete(1.0, "end")
    result_box.insert("end", f"Detected text:\n{text}\n")
    dates = find_dates(text)
    if not dates:
        speak("No valid dates detected.")
        result_box.insert("end", "\nNo valid dates found.")
        return
    dates.sort()
    if len(dates) >= 2:
        mfg, exp = dates[0], dates[-1]
        result_box.insert("end", f"\nManufacturing Date: {mfg.strftime('%d-%m-%Y')}")
        result_box.insert("end", f"\nExpiry Date: {exp.strftime('%d-%m-%Y')}")
        if datetime.now() > exp:
            status = "⚠️ This medicine has expired."
        else:
            status = "✅ This medicine is valid."
        result_box.insert("end", f"\n{status}")
        speak(f"The medicine was manufactured on {mfg.strftime('%d-%m-%Y')} and expires on {exp.strftime('%d-%m-%Y')}. {status}")
    else:
        single_date = dates[0].strftime("%d-%m-%Y")
        result_box.insert("end", f"\nOnly one date found: {single_date}")
        speak(f"I found one date: {single_date}. Can't confirm if it's expiry or manufacturing.")
