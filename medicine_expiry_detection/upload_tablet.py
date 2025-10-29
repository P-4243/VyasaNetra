from ocr_module import extract_text_from_image
from ai_classifier import interpret_medicine_info
from voice_module import speak  # Optional voice feedback

def upload_and_analyze():
    image_path = input("Enter the image path: ")

    print("\n🔍 Extracting text from image...")
    text = extract_text_from_image(image_path)
    print("\n📝 Extracted Text:\n", text)

    print("\n🤖 Analyzing with Gemini AI...")
    result = interpret_medicine_info(text)

    print("\n✅ AI Result:\n", result)
    speak(result)  # Comment this out if not using voice output

if __name__ == "__main__":
    upload_and_analyze()
