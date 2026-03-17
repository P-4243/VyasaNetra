import re
import cv2
from object_detector import detect_objects
from gemini_helper import describe_objects
from voice_helper import speak,listen_for_command
# from voice_module import listen_for_command

# ------------------ SMART OBJECT EXTRACTION ------------------
def extract_object_name(user_text):
    """
    Extracts only meaningful words (like 'wallet', 'phone') 
    and removes filler words (like 'find', 'my', 'please').
    """
    words = re.findall(r"\b[a-zA-Z]+\b", user_text.lower())
    ignore_words = {
        'i', 'want', 'to', 'find', 'locate', 'show', 'me', 'the', 'a', 'an',
        'please', 'say', 'what', 'you', 'my', 'where', 'it', 'is', 'can', 'do'
    }
    filtered = [w for w in words if w not in ignore_words]
    return " ".join(filtered) if filtered else None


# ------------------ MAIN APP LOGIC ------------------
def main():
    target_object = None

    speak("Say what you want to find.")
    command = listen_for_command()

    # Extract the actual target object name
    target_object = extract_object_name(command)

    if not target_object:
        speak("I didn’t hear any object name clearly.")
        return

    speak(f"Okay, I’ll look for your {target_object}.")

    # Start camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Camera not detected.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect objects using YOLO
        frame, detected = detect_objects(frame)
        cv2.imshow("Object Detection", frame)

        if detected:
            print("Detected:", detected)

            # If target is found
            if target_object in detected:
                desc = describe_objects([target_object])

                # Clean Gemini’s text before speaking
                clean_desc = desc.replace("*", "").replace("**", "").replace("#", "").replace("-", "")
                #speak(f"I found your {target_object}. Here’s what I think.")
                #speak(clean_desc)
                break

            # If not found yet, don’t keep repeating constantly
            else:
                print(f"Still looking for your {target_object}...")

        # Press 'q' to quit manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #speak("Stopping detection.")
    cap.release()
    cv2.destroyAllWindows()


# ------------------ RUN THE APP ------------------
if __name__ == "__main__":
    main()
