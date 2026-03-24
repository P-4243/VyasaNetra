from voice_module import speak, listen

# Import features
from object_search.main import run_object_search
from medicine_expiry_detection.camera_module import process_camera_image

def show_menu():
    speak("Welcome to VyasNetra.")
    speak("Say 1 to search for an object.")
    speak("Say 2 to add money to wallet.")
    speak("Say 3 for currency identification.")
    speak("Say 4 for medicine expiry detection.")
    speak("Say exit to close the app.")


def get_choice():
    command = listen()
    print("Command received:", command)

    if not command:
        return None

    # Smart matching
    if "one" in command or "object" in command:
        return 1
    elif "two" in command or "wallet" in command:
        return 2
    elif "three" in command or "currency" in command:
        return 3
    elif "four" in command or "medicine" in command:
        return 4
    elif "exit" in command or "stop" in command:
        return "exit"

    return None


def main():
    while True:
        show_menu()

        speak("Please say your choice.")
        choice = get_choice()

        if choice == 1:
            speak("Starting object search.")
            run_object_search()

        elif choice == 2:
            speak("Wallet feature is not implemented yet.")

        elif choice == 3:
            speak("Currency identification coming soon.")

        elif choice == 4:
            speak("Starting medicine expiry detection.")
            process_camera_image()

        elif choice == "exit":
            speak("Goodbye.")
            break

        else:
            speak("I did not understand. Please try again.")


if __name__ == "__main__":
    main()