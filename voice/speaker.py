import pyttsx3
import threading

_engine = None
_engine_lock = threading.Lock()


def create_engine():
    engine = pyttsx3.init("sapi5")

    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")

    if voices:
        engine.setProperty("voice", voices[0].id)

    return engine


def speak(text):

    global _engine

    if not text:
        return

    text = str(text).strip()

    if not text:
        return

    try:

        # Each speech gets a fresh SAPI engine.
        # This avoids SAPI5 getting stuck after previous speech.

        with _engine_lock:

            print(
                "🔊 ARCHON SPEAKING:",
                text
            )

            engine = create_engine()

            _engine = engine

            engine.say(text)

            engine.runAndWait()

            try:
                engine.stop()
            except Exception:
                pass

            _engine = None

            print(
                "🔊 ARCHON FINISHED SPEAKING"
            )

    except Exception as e:

        print(
            "❌ Speaker error:",
            e
        )

        _engine = None


def stop_speaking():

    global _engine

    try:

        engine = _engine

        if engine is not None:

            print(
                "🛑 Stopping ARCHON speech..."
            )

            engine.stop()

    except Exception as e:

        print(
            "❌ Stop speaker error:",
            e
        )