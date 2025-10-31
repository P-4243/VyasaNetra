
import cv2
from object_detector import detect_objects
from gemini_helper import describe_objects
from voice_helper import speak
from voice_module import listen_for_command

def main():
    target_object = None

    speak("Welcome! Say what you want to find.")
    command = listen_for_command()

    # Extract target object from voice command
    for word in ["find", "locate", "where", "my", "the"]:
        command = command.replace(word, "")# It removes common filler words ("find", "my", etc.) to isolate the name of the object
    target_object = command.strip()

    if not target_object:
        speak("I didn’t hear any object name.")
        return

    speak(f"Okay, I’ll look for your {target_object}.")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Camera not detected.")
        return

    while True:
        ret, frame = cap.read()#ret is a boolean indicating success
        if not ret:
            break

        frame, detected = detect_objects(frame)
        #So, frame holds an image. second value returned (the list of object names) and assigns it to the detected variable.
        cv2.imshow("Object Detection", frame)#Displays the frame in a window titled "Object Detection".

        if detected:
            print("Detected:", detected)
            if target_object in detected:
                desc = describe_objects([target_object])
                print("Gemini says:", desc)

                # Clean the Gemini output for voice (remove markdown, bullets)
                clean_desc = desc.replace("*", "").replace("**", "").replace("#", "").replace("-", "")
                speak(f"I found your {target_object}. Here’s what I think.")
                speak(clean_desc)
                break

            else:
                speak(f"Still looking for your {target_object}.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            #It takes a single character (like 'q') and returns its integer ASCII value


    speak("Stopping detection.")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
