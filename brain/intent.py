def get_intent(command):

    command = command.lower()

    # Browser
    if "chrome" in command and (
        "open" in command or
        "launch" in command or
        "start" in command
    ):
        return "OPEN_CHROME"

    if (
        command.startswith("search") or
        "google" in command or
        "look up" in command or
        "find" in command
    ):
        return "SEARCH"

    if "new tab" in command or "open new tab" in command:
        return {
            "intent": "NEW_TAB"
        }

    if "close tab" in command:
        return {
            "intent": "CLOSE_TAB"
        }

    if "go back" in command or "back" == command:
        return {
            "intent": "GO_BACK"
        }

    if "refresh" in command or "refresh page" in command:
        return {
            "intent": "REFRESH_PAGE"
        }

    # AI
    return "AI"