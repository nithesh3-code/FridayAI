from voice.speaker import speak, stop_speaking
from voice.listener import listen

import core.router as router
from brain.ai import ask_ai

import threading


class Assistant:

    def __init__(self, status_callback=None):

        self.status_callback = status_callback

        self.stop_event = threading.Event()
        self.running = False

        speak("Hello! I am ARCHON.")

        self.update_status("SYSTEM READY")

    def update_status(self, status):

        if self.status_callback:
            self.status_callback(status)

    # -----------------------------------------
    # MAIN ARCHON LOOP
    # -----------------------------------------

    def run(self):

        self.running = True
        self.stop_event.clear()

        while self.running and not self.stop_event.is_set():

            # ---------------------------------
            # LISTEN
            # ---------------------------------

            self.update_status("LISTENING")

            command = listen()

            # STOPPED while listening
            if self.stop_event.is_set():
                break

            if not command:

                self.update_status(
                    "VOICE NOT UNDERSTOOD"
                )

                continue

            self.update_status(
                f"COMMAND: {command}"
            )

            # ---------------------------------
            # EXIT
            # ---------------------------------

            if "exit" in command.lower():

                self.update_status(
                    "SHUTTING DOWN"
                )

                speak("Goodbye!")

                self.running = False
                break

            # ---------------------------------
            # PROCESS COMMAND
            # ---------------------------------

            self.update_status(
                "PROCESSING"
            )

            result = router.handle_command(command)

            # STOPPED while processing
            if self.stop_event.is_set():
                break

            self.update_status(
                f"TASK: {router.current_task}"
            )

            # ---------------------------------
            # ROUTER RESULT
            # ---------------------------------

            if result:

                print(
                    "ARCHON:",
                    result
                )

                self.update_status(
                    "SPEAKING"
                )

                print(
                    "🔊 ABOUT TO SPEAK ROUTER ANSWER"
                )

                speak(result)

                print(
                    "🔊 ROUTER ANSWER SPEECH FINISHED"
                )

                continue

            # ---------------------------------
            # AI
            # ---------------------------------

            self.update_status(
                "THINKING"
            )

            router.current_task = "AI"

            self.update_status(
                f"TASK: {router.current_task}"
            )

            reply = ask_ai(command)

            # STOPPED while AI was processing
            if self.stop_event.is_set():
                break

            print(
                "AI:",
                reply
            )

            # ---------------------------------
            # SPEAK AI ANSWER
            # ---------------------------------

            self.update_status(
                "SPEAKING"
            )

            print(
                "🔊 ABOUT TO SPEAK AI ANSWER"
            )

            speak(reply)

            print(
                "🔊 AI ANSWER SPEECH FINISHED"
            )

            if self.stop_event.is_set():
                break

            self.update_status(
                "LISTENING"
            )

        # ---------------------------------
        # ARCHON STOPPED
        # ---------------------------------

        self.running = False

        self.update_status(
            "ARCHON STOPPED"
        )

        print(
            "🛑 ARCHON assistant loop stopped."
        )

    def stop(self):

        print("🛑 STOPPING ARCHON...")

        self.running = False

        self.stop_event.set()

        try:
            stop_speaking()
        except Exception as e:
            print(
                "Speaker stop error:",
                e
            )

        self.update_status(
            "STOPPING"
        )