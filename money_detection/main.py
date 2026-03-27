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

# ------------------ HELPER ------------------

def suggest_payment(wallet, amount):
    available = []

    for note, count in wallet.items():
        available += [note] * count

    available.sort()

    for val in available:
        if val >= amount:
            return val

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

    text = text.lower().strip()

    if text.isdigit():
        return int(text)

    if text in words_to_numbers:
        return words_to_numbers[text]

    return None


# ------------------ MAIN FLOW ------------------

def run_money_detection():

    # ------------------ GET AMOUNT ------------------
    while True:
        speak("How much do you want to pay?")
        command = listen()

        amount = parse_amount(command)

        if amount is not None:
            speak(f"You said {amount} rupees.")
            break

        speak("Sorry, I didn't understand. Please say the amount again.")

    # ------------------ CHECK WALLET ------------------
    suggested = suggest_payment(wallet, amount)

    if suggested is None:
        speak("You do not have enough money.")
        return

    # ------------------ SUGGEST PAYMENT ------------------
    if suggested != amount:
        speak(f"You don’t have exact amount. Give {suggested} rupees.")
    else:
        speak(f"You can give {suggested} rupees.")

    # ------------------ VERIFY NOTE ------------------
    while True:
        speak(f"Please show {suggested} rupee note.")

        detected = detect_currency()

        if detected is None:
            speak("Could not detect note. Try again.")
            continue

        if detected == suggested:
            speak("Correct note. You can give it to the shopkeeper.")
            wallet[suggested] -= 1
            break
        else:
            speak(f"This is {detected} rupees. Please show {suggested} rupees.")

    # ------------------ HANDLE CHANGE ------------------
    change = suggested - amount

    if change > 0:
        speak(f"You should receive {change} rupees as change.")
        speak("Please show the change one note at a time.")

        received = 0

        while received < change:
            detected = detect_currency()

            if detected is None:
                speak("Could not detect. Try again.")
                continue

            received += detected
            speak(f"Detected {detected} rupees. Total received {received}.")

            # Update wallet
            if detected in wallet:
                wallet[detected] += 1
            else:
                wallet[detected] = 1

        # ------------------ VALIDATION ------------------
        if received == change:
            speak("You received correct change.")
        elif received > change:
            speak("You received extra money.")
        else:
            speak("You received less money. Please check.")

    # ------------------ FINAL WALLET ------------------
    print("Updated Wallet:", wallet)