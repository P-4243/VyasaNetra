from voice_module import speak, listen

# Import features
from object_search.main import run_object_search
from money_detection.main import run_money_detection
from medicine_expiry_detection.camera_module import process_camera_image


# ------------------ MENU ------------------

def show_menu():
    speak("Welcome to VyasNetra.")
    speak("Say 1 or say object search.")
    speak("Say 2 or say payment assistant.")
    speak("Say 3 or say currency identification.")
    speak("Say 4 or say medicine detection.")
    speak("Say exit to close the app.")


# ------------------ SMART CHOICE ------------------

def get_choice():
    for _ in range(3):  # retry 3 times
        command = listen()
        print("Command received:", command)

        if not command:
            speak("Please say your choice again.")
            continue

        command = command.lower()

        # ✅ Strong matching
        if any(word in command for word in ["1", "one", "object"]):
            return 1

        elif any(word in command for word in ["2", "two", "payment", "wallet"]):
            return 2

        elif any(word in command for word in ["3", "three", "currency"]):
            return 3

        elif any(word in command for word in ["4", "four", "medicine"]):
            return 4

        elif any(word in command for word in ["exit", "stop", "quit"]):
            return "exit"

        else:
            speak("I did not understand. Try again.")

    return None


# ------------------ MAIN LOOP ------------------

def main():
    while True:
        show_menu()

        speak("Please say your choice.")
        choice = get_choice()

        if choice == 1:
            speak("Starting object search.")
            run_object_search()

        elif choice == 2:
            speak("Starting payment assistant.")
            run_money_detection()

        elif choice == 3:
            speak("Payment assistant starting.")
    
            from money_detection.main import run_money_detection
            run_money_detection()

        elif choice == 4:
            speak("Starting medicine expiry detection.")
            process_camera_image()

        elif choice == "exit":
            speak("Goodbye.")
            break

        else:
            speak("Returning to main menu.")


# ------------------ RUN ------------------

if __name__ == "__main__":
    main()