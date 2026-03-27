# import cv2
# from matplotlib.pyplot import gray
# from matplotlib.pyplot import gray
# import pytesseract
# import re
# import time
# from money_detection.voice_module import speak


# def extract_amount(text):
#     text = text.replace("O", "0").replace("o", "0").replace("l", "1")

#     matches = re.findall(r'\d+', text)
#     valid_notes = [10, 20, 50, 100, 200, 500]

#     for m in matches:
#         num = int(m)
#         if num in valid_notes:
#             return num

#     return None

# def detect_currency():
#     speak("Opening camera. Show the note clearly.")

#     cap = cv2.VideoCapture(2)

#     if not cap.isOpened():
#         speak("Camera not detected.")
#         return None

#     last_detected = None
#     stable_count = 0
#     start_time = time.time()

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Increase contrast
#         gray = cv2.equalizeHist(gray)

#         # Thresholding (VERY IMPORTANT)
#         _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#         # Optional blur
#         thresh = cv2.GaussianBlur(thresh, (3,3), 0)

#         text = pytesseract.image_to_string(thresh, config='--psm 6')

#         amount = extract_amount(text)

#         # ---------------- STABILITY LOGIC ----------------
#         if amount == last_detected and amount is not None:
#             stable_count += 1
#         else:
#             stable_count = 0
#             last_detected = amount

#         # ---------------- AUTO CAPTURE ----------------
#         if stable_count > 5:   # 🔥 reduced threshold
#             speak(f"Detected {amount} rupees.")
#             cap.release()
#             cv2.destroyAllWindows()
#             return amount

#         # ---------------- USER FEEDBACK ----------------
#         if amount:
#             cv2.putText(frame, f"Detected: {amount}",
#                         (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
#         else:
#             cv2.putText(frame, "Align note properly",
#                         (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

#         cv2.imshow("Currency Detection", frame)

#         # ---------------- TIMEOUT SAFETY ----------------
#         if time.time() - start_time > 10:
#             speak("Could not detect clearly. Try again.")
#             break

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return None