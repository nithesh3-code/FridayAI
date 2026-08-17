import subprocess
import time
import os

import pyautogui
import pyperclip
import requests


# =========================================================
# CHROME CONFIG
# =========================================================

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEBUG_PORT = 9222
PROFILE_PATH = r"E:\FridayAI\chrome_profile"


# =========================================================
# VS CODE
# =========================================================



# =========================================================
# CREATE FILE
# =========================================================

def create_file(file_path, content=""):

    try:

        folder = os.path.dirname(file_path)

        if folder:
            os.makedirs(
                folder,
                exist_ok=True
            )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        return f"File created: {file_path}"

    except Exception as e:

        return f"Failed to create file: {e}"


# =========================================================
# UPDATE EXISTING FILE
# =========================================================

def write_file(file_path, content):

    try:

        if not os.path.exists(file_path):

            return f"File does not exist: {file_path}"

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(content)

        return f"File updated: {file_path}"

    except Exception as e:

        return f"Failed to update file: {e}"


# =========================================================
# RUN PYTHON FILE
# =========================================================

def run_python_file(file_path):

    try:

        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode == 0:

            return (
                "PROGRAM RAN SUCCESSFULLY\n"
                + output
            )

        return (
            "PROGRAM ERROR\n"
            + error
        )

    except subprocess.TimeoutExpired:

        return (
            "PROGRAM TIMED OUT after 30 seconds."
        )

    except Exception as e:

        return f"Failed to run program: {e}"


# =========================================================
# OPEN CHROME
# =========================================================

def open_chrome():

    command = [
        CHROME_PATH,
        f"--remote-debugging-port={DEBUG_PORT}",
        "--remote-debugging-address=127.0.0.1",
        f"--user-data-dir={PROFILE_PATH}",
        "--no-first-run",
        "--no-default-browser-check"
    ]

    try:

        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        for _ in range(10):

            time.sleep(1)

            try:

                response = requests.get(
                    f"http://127.0.0.1:{DEBUG_PORT}/json/version",
                    timeout=2
                )

                if response.status_code == 200:

                    return "Chrome is open and ready."

            except requests.exceptions.RequestException:

                continue

        return (
            "Chrome opened, but ARCHON could not connect "
            "to Chrome debugging port 9222."
        )

    except Exception as e:

        return f"Failed to start Chrome: {e}"


# =========================================================
# GOOGLE SEARCH
# =========================================================

def search_google(query):

    try:

        open_chrome()

        time.sleep(2)

        pyperclip.copy(query)

        pyautogui.hotkey(
            "ctrl",
            "l"
        )

        time.sleep(0.5)

        pyautogui.hotkey(
            "ctrl",
            "v"
        )

        time.sleep(0.2)

        pyautogui.press("enter")

        return f"Searching Google for {query}"

    except Exception as e:

        return f"Search failed: {e}"


# =========================================================
# NEW TAB
# =========================================================

def new_tab():

    pyautogui.hotkey(
        "ctrl",
        "t"
    )

    time.sleep(1)

    return "New tab opened."


# =========================================================
# CLOSE TAB
# =========================================================

def close_tab():

    pyautogui.hotkey(
        "ctrl",
        "w"
    )

    time.sleep(1)

    return "Tab closed."


# =========================================================
# GO BACK
# =========================================================

def go_back():

    pyautogui.hotkey(
        "alt",
        "left"
    )

    time.sleep(1)

    return "Going back."


# =========================================================
# REFRESH PAGE
# =========================================================

def refresh_page():

    pyautogui.press(
        "f5"
    )

    time.sleep(1)

    return "Page refreshed."


# =========================================================
# CLOSE CHROME
# =========================================================

def close_chrome():

    pyautogui.hotkey(
        "alt",
        "f4"
    )

    time.sleep(1)

    return "Chrome closed."


# =========================================================
# GET CURRENT URL
# =========================================================

def get_current_url():

    try:

        pyautogui.hotkey(
            "ctrl",
            "l"
        )

        time.sleep(0.3)

        pyautogui.hotkey(
            "ctrl",
            "c"
        )

        time.sleep(0.3)

        url = pyperclip.paste()

        pyautogui.press(
            "escape"
        )

        return url

    except Exception:

        return None


# =========================================================
# YOUTUBE SEARCH
# =========================================================

def search_youtube(query):

    try:

        open_chrome()

        time.sleep(2)

        url = (
            "https://www.youtube.com/results?search_query="
            + requests.utils.quote(query)
        )

        pyautogui.hotkey(
            "ctrl",
            "l"
        )

        time.sleep(0.5)

        pyperclip.copy(url)

        pyautogui.hotkey(
            "ctrl",
            "v"
        )

        time.sleep(0.2)

        pyautogui.press(
            "enter"
        )

        return f"Searching YouTube for {query}"

    except Exception as e:

        return f"YouTube search failed: {e}"

def run_java_file(file_path):
    try:
        file_path = os.path.abspath(file_path)

        folder = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        if not filename.lower().endswith(".java"):
            return "Java execution failed: file is not a .java file."

        class_name = os.path.splitext(filename)[0]

        # Compile
        compile_result = subprocess.run(
            ["javac", filename],
            cwd=folder,
            capture_output=True,
            text=True,
            timeout=30
        )

        if compile_result.returncode != 0:
            return (
                "JAVA COMPILATION FAILED\n"
                + compile_result.stderr.strip()
            )

        # Run
        run_result = subprocess.run(
            ["java", class_name],
            cwd=folder,
            capture_output=True,
            text=True,
            timeout=30
        )

        if run_result.returncode != 0:
            return (
                "JAVA PROGRAM FAILED\n"
                + run_result.stderr.strip()
            )

        output = run_result.stdout.strip()

        return (
            "JAVA PROGRAM RAN SUCCESSFULLY\n"
            + (output if output else "[No output]")
        )

    except subprocess.TimeoutExpired:
        return "Java program timed out."

    except Exception as e:
        return f"Java execution error: {e}"


def run_javascript_file(file_path):
    try:
        file_path = os.path.abspath(file_path)

        if not file_path.lower().endswith(".js"):
            return "JavaScript execution failed: file is not a .js file."

        folder = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        # Check Node.js
        node_check = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if node_check.returncode != 0:
            return (
                "NODE.JS NOT INSTALLED\n"
                "ARCHON cannot run JavaScript yet."
            )

        result = subprocess.run(
            ["node", filename],
            cwd=folder,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return (
                "JAVASCRIPT PROGRAM FAILED\n"
                + result.stderr.strip()
            )

        output = result.stdout.strip()

        return (
            "JAVASCRIPT PROGRAM RAN SUCCESSFULLY\n"
            + (output if output else "[No output]")
        )

    except subprocess.TimeoutExpired:
        return "JavaScript program timed out."

    except Exception as e:
        return f"JavaScript execution error: {e}"