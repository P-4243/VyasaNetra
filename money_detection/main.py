from money_detection.voice_module import speak, listen
from money_detection.yolo_currency_detector import detect_currency

# ------------------ WALLET ------------------
wallet = {
    10: 1,
    20: 1,
    50: 0,
    100: 1,
    200: 0,
    500: 0
}

def get_wallet_total(wallet):
    return sum(note * count for note, count in wallet.items())


# ------------------ HELPER ------------------

from itertools import combinations

def suggest_payment(wallet, amount):
    available = []

    for note, count in wallet.items():
        available += [note] * count

    # Try all combinations
    for r in range(1, len(available) + 1):
        for combo in combinations(available, r):
            if sum(combo) >= amount:
                return list(combo)

    return None


# ------------------ PARSE AMOUNT ------------------

def parse_amount(text):
    words_to_numbers = {
        "ten": 10,
        "twenty": 20,
        "fifty": 50,
        "hundred": 100,
        "one hundred": 100,
        "two hundred": 200,
        "five hundred": 500
    }

    if not text:
        return None

    text = text.lower().strip()

    if text.isdigit():
        return int(text)

    return words_to_numbers.get(text, None)


# ------------------ MAIN FLOW ------------------

def run_money_detection():

    # -------- GET AMOUNT --------
    while True:
        speak("How much do you want to pay?")
        command = listen()

        amount = parse_amount(command)

        if amount is not None:
            speak(f"You said {amount} rupees.")
            break

        speak("Sorry, I didn't understand. Please say again.")

    # -------- CHECK WALLET --------
    suggested_notes = suggest_payment(wallet, amount)

    if suggested_notes is None:
        speak("You do not have enough money.")
        return

    total_given = sum(suggested_notes)

    speak(f"Give notes: {suggested_notes}. Total {total_given} rupees.")

    # -------- VERIFY EACH NOTE --------
    for note in suggested_notes:
        while True:
            speak(f"Please show {note} rupee note.")
            detected = detect_currency()

            if detected is None:
                speak("Could not detect. Try again.")
                continue

            if detected == note:
                speak("Correct note.")
                
                if wallet.get(note, 0) > 0:
                    wallet[note] -= 1
                break
            else:
                speak(f"This is {detected}. Please show {note} rupees.")

    speak("You can give the money.")

    # -------- HANDLE CHANGE --------
    change = total_given - amount

    if change > 0:
        speak(f"You should receive {change} rupees.")
        speak("Show change one note at a time.")

        received = 0

        while received < change:
            detected = detect_currency()

            if detected is None:
                speak("Could not detect. Try again.")
                continue

            received += detected
            speak(f"Detected {detected}. Total received {received}.")

            wallet[detected] = wallet.get(detected, 0) + 1

            if received > change:
                speak("Extra money detected. Stop.")
                break

        # -------- VALIDATION --------
        if received == change:
            speak("Correct change received.")
        elif received > change:
            speak("You received extra money.")
        else:
            speak("You received less money.")

    print("Updated Wallet:", wallet)


# ------------------ MANAGE WALLET ------------------

def manage_wallet():
    total = get_wallet_total(wallet)
    speak(f"Your wallet has {total} rupees.")

    while True:
        speak("Do you want to add money? Say yes or no.")
        response = listen()

        if not response:
            speak("I did not hear anything.")
            continue

        if "yes" in response:
            speak("Show the note to add.")

            detected = detect_currency()

            if detected is None:
                speak("Could not detect note.")
                return

            wallet[detected] = wallet.get(detected, 0) + 1

            speak(f"{detected} rupees added.")

            new_total = get_wallet_total(wallet)
            speak(f"Now wallet has {new_total} rupees.")
            break

        elif "no" in response or "exit" in response:
            speak("Returning to main menu.")
            break

        else:
            speak("Say yes or no.")