from tkinter import filedialog, Tk, Text, END
from ocr_module import extract_text_from_image, analyze_text
from tkinter import Tk, Text

def upload_tablet_image():
    # Hide the main Tkinter window (so only file dialog opens)
    root = Tk()
    root.withdraw()

    # Open file chooser
    image_path = filedialog.askopenfilename(
        title="Select Medicine Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
    )

    if not image_path:
        print("❌ No image selected.")
        return

    print(f"✅ Selected image: {image_path}")

    # Extract text from image
    text = extract_text_from_image(image_path)
    print("\n--- Extracted Text ---\n")
    print(text)

    # Temporary text box to reuse analyze_text() function
    temp_root = Tk()
    temp_root.title("Tablet Info")
    result_box = Text(temp_root, width=60, height=15)
    result_box.pack(padx=10, pady=10)

    # Analyze the OCR text (checks for expiry/manufacturing)
    analyze_text(text, result_box)

    temp_root.mainloop()


if __name__ == "__main__":
    upload_tablet_image()
