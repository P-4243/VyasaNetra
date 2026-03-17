import speech_recognition as sr

for i, mic in enumerate(sr.Microphone.list_microphone_names()):
    print(i, mic)