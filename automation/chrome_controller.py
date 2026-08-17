import subprocess
import time
import pyautogui
import pyperclip
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
DEBUG_PORT = 9222
PROFILE_PATH = r"E:\FridayAI\chrome_profile"


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

        # Give Chrome enough time to start
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


def search_google(query):

    try:

        # Make sure Chrome is running first
        open_chrome()

        time.sleep(2)

        # Copy query to clipboard
        pyperclip.copy(query)

        # Focus Chrome address bar
        pyautogui.hotkey("ctrl", "l")
        time.sleep(0.5)

        # Paste query
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.2)

        # Search
        pyautogui.press("enter")

        return f"Searching Google for {query}"

    except Exception as e:

        return f"Search failed: {e}"

def new_tab():
    pyautogui.hotkey("ctrl", "t")
    time.sleep(1)
    return "New tab opened."


def close_tab():
    pyautogui.hotkey("ctrl", "w")
    time.sleep(1)
    return "Tab closed."


def go_back():
    pyautogui.hotkey("alt", "left")
    time.sleep(1)
    return "Going back."


def refresh_page():
    pyautogui.press("f5")
    time.sleep(1)
    return "Page refreshed."

def close_chrome():
    pyautogui.hotkey("alt", "f4")
    time.sleep(1)
    return "Chrome closed."

def get_current_url():

    try:
        pyautogui.hotkey("ctrl", "l")
        time.sleep(0.3)

        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.3)

        import pyperclip

        url = pyperclip.paste()

        pyautogui.press("escape")

        return url

    except Exception as e:
        return None

def search_youtube(query):

    try:

        # Make sure Chrome is open
        open_chrome()

        time.sleep(2)

        # Open YouTube search directly
        url = (
            "https://www.youtube.com/results?search_query="
            + requests.utils.quote(query)
        )

        pyautogui.hotkey("ctrl", "l")
        time.sleep(0.5)

        pyperclip.copy(url)

        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.2)

        pyautogui.press("enter")

        return f"Searching YouTube for {query}"

    except Exception as e:

        return f"YouTube search failed: {e}"

def play_first_youtube_result():

    try:

        options = Options()

        options.add_experimental_option(
            "debuggerAddress",
            "127.0.0.1:9222"
        )

        driver = webdriver.Chrome(
            options=options
        )

        time.sleep(3)

        # Find the first video result
        videos = driver.find_elements(
            "css selector",
            "a#video-title"
        )

        if not videos:
            return "I couldn't find a YouTube video."

        # Open the first result
        videos[0].click()

        time.sleep(3)

        return "Playing the first YouTube video."

    except Exception as e:

        return f"Could not play YouTube video: {e}"