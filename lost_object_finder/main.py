import re
import cv2
import time
from object_detector import detect_objects
from gemini_helper import describe_objects
from navigation_helper import bbox_to_guidance
from voice_helper import speak, listen_for_command


def extract_object_name(user_text):
    """Extracts only meaningful words like 'wallet', 'phone', etc."""
    words = re.findall(r"\b[a-zA-Z]+\b", user_text.lower())
    ignore_words = {
        'i', 'want', 'to', 'find', 'locate', 'show', 'me', 'the', 'a', 'an',
        'please', 'say', 'what', 'you', 'my', 'where', 'it', 'is', 'can', 'do'
    }
    filtered = [w for w in words if w not in ignore_words]
    return " ".join(filtered) if filtered else None


def main():
    speak("Hello! I’m your assistant. What do you want to find?")
    command = listen_for_command()
    target_object = extract_object_name(command)

    if not target_object:
        speak("I didn’t hear any object name clearly. Please try again later.")
        return

    speak(f"Okay, I’ll look for your {target_object}. Please hold still.")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Camera not detected. Please check your camera connection.")
        return

    last_speak_time = time.time()
    repeat_delay = 3  # seconds between repeated guidance

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, detected, boxes_dict = detect_objects(frame)
        cv2.imshow("Object Detection", frame)

        if target_object in boxes_dict:
            # Take the first detected bounding box for target
            bbox = boxes_dict[target_object][0]
            H, W, _ = frame.shape
            guidance = bbox_to_guidance(bbox, (W, H))

            speak(f"I can see your {target_object}. {guidance['guidance_text']}")

            if guidance["distance_category"] == "very close":
                speak(f"You’ve almost reached your {target_object}. One last step forward.")
                time.sleep(2)
                speak(f"You’ve reached your {target_object}. May I leave now?")
                response = listen_for_command().lower()

                if any(word in response for word in ["yes", "yeah", "sure", "ok", "okay", "you may"]):
                    speak("Glad I could help. Goodbye!")
                    break
                else:
                    speak("Okay, I’ll stay with you a bit longer.")
                    time.sleep(4)
                continue

        else:
            if time.time() - last_speak_time > repeat_delay:
                speak(f"Still scanning for your {target_object}. Please stay still.")
                last_speak_time = time.time()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            speak("You chose to quit. Stopping detection.")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
