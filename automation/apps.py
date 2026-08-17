import os

def open_app(command):

    apps = {
        "chrome": "chrome",
        "notepad": "notepad",
        "calculator": "calc",
        "paint": "mspaint",
        "cmd": "cmd",
    }

    for app, exe in apps.items():
        if f"open {app}" in command:
            os.system(f"start {exe}")
            return f"Opening {app}"

    return None


def close_app(command):

    processes = {
        "chrome": "chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
    }

    for app, process in processes.items():
        if f"close {app}" in command:
            os.system(f"taskkill /IM {process} /F")
            return f"Closing {app}"

    return None