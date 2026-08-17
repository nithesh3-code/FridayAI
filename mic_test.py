import speech_recognition as sr

print("=== MICROPHONES ===")

for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(i, "->", name)

print("\n=== DEFAULT MICROPHONE TEST ===")

r = sr.Recognizer()

with sr.Microphone(device_index=1) as source:
    print("Speak now...")

    r.adjust_for_ambient_noise(
        source,
        duration=8
    )

    print("Listening...")

    audio = r.listen(
        source,
        timeout=10,
        phrase_time_limit=10
    )
try:
    text = r.recognize_google(audio)
    print("YOU SAID:", text)

except sr.UnknownValueError:
    print("Microphone received audio, but speech was not understood.")

except sr.RequestError as e:
    print("Google recognition error:", e)

except Exception as e:
    print("ERROR:", e)