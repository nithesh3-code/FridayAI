import speech_recognition as sr


recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

recognizer.pause_threshold = 0.8
recognizer.non_speaking_duration = 0.5


def listen():

    try:

        with sr.Microphone(device_index=1) as source:

            print("🎤 Listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            try:

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            except sr.WaitTimeoutError:

                print("No speech detected.")

                return ""

    except Exception as e:

        print(
            "❌ Microphone error:",
            e
        )

        return ""

    try:

        text = recognizer.recognize_google(audio)

        text = text.lower().strip()

        print(
            "You:",
            text
        )

        return text

    except sr.UnknownValueError:

        print(
            "Sorry, I didn't understand."
        )

        return ""

    except sr.RequestError as e:

        print(
            "Speech recognition network error:",
            e
        )

        return ""

    except Exception as e:

        print(
            "❌ Recognition error:",
            e
        )

        return ""