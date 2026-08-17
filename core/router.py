from automation.chrome_controller import (
    open_chrome,
    search_google,
    search_youtube,
    play_first_youtube_result,
    new_tab,
    close_tab,
    close_chrome,
    go_back,
    refresh_page,
)

from brain.code_agent import build_python_project
from brain.code_agent import build_python_project
from agents.browser_agent import get_current_page_text
from brain.ai import summarize_text, ask_about_page
from brain.vision import analyze_image
from brain.visual_state import get_image

current_page_active = False
current_page_topic = ""
current_task = "IDLE"

def is_related_to_page(command):
    if not current_page_topic:
        return False

    topic_words = current_page_topic.lower().split()

    for word in topic_words:
        if len(word) > 2 and word in command:
            return True

    return False

def handle_command(command):

    global current_page_active, current_page_topic, current_task
    command = command.lower().strip()

    # -------------------------
    # Chrome controls
    # -------------------------

    if "open chrome" in command:
        current_task = "BROWSER"
        return open_chrome()

    if "close chrome" in command:
        current_task = "BROWSER"
        current_page_active = False
        current_page_topic = ""
        return close_chrome()

    if "open new tab" in command or command == "new tab":
        current_task = "BROWSER"
        current_page_active = False
        current_page_topic = ""
        return new_tab()

    if "close tab" in command:
        return close_tab()

    if "go back" in command:
        return go_back()

    if "refresh page" in command or command == "refresh":
        return refresh_page()

    # -------------------------
    # Vision / Image questions
    # -------------------------

    image_path = get_image()

    if image_path:

        explicit_vision_words = [
            "image",
            "picture",
            "photo",
            "screenshot",
            "shown",
            "visible",
            "look like"
        ]

        natural_vision_phrases = [
            "what is he wearing",
            "what is she wearing",
            "what are they wearing",
            "what is he doing",
            "what is she doing",
            "what are they doing",
            "what is happening",
            "what color is",
            "what colour is",
            "is there",
            "are there",
            "who is in",
            "what objects",
            "which objects",
            "describe",
            "where is",
            "how many",
            "can you see"
        ]

        # Words that usually refer to something
        # visible in the currently loaded image.
        visual_reference_words = [
            # People
            "he",
            "she",
            "they",
            "him",
            "her",
            "them",
            "his",
            "their",
            "man",
            "men",
            "male",
            "woman",
            "women",
            "female",
            "person",
            "people",
            "boy",
            "girl",
            "child",
            "children",

            # Body / appearance
            "shirt",
            "t-shirt",
            "clothes",
            "clothing",
            "dress",
            "pants",
            "hair",
            "face",
            "eyes",
            "nose",
            "mouth",
            "beard",
            "mustache",
            "skin",
            "body",

            # Objects
            "object",
            "objects",
            "thing",
            "things",
            "phone",
            "laptop",
            "computer",
            "car",
            "chair",
            "table",
            "bag",
            "book",

            # Environment
            "background",
            "room",
            "wall",
            "door",
            "window",
            "kitchen",
            "street",

            # Visual properties
            "color",
            "colour",
            "size",
            "shape",
            "position",
            "left",
            "right",
            "front",
            "behind",
            "next",
            "near",
            "beside"
        ]

        is_explicit_vision = any(
            word in command
            for word in explicit_vision_words
        )

        is_natural_vision = any(
            phrase in command
            for phrase in natural_vision_phrases
        )

        is_visual_reference = any(
            word in command.split()
            for word in visual_reference_words
        )

        # If an image is loaded and the question
        # contains a visual reference, use Vision.
        if (
            is_explicit_vision
            or is_natural_vision
            or is_visual_reference
        ):
            current_task = "VISION"

            return analyze_image(
                image_path,
                command
            )


    # -------------------------
    # ARCHON CODING AGENT
    # -------------------------

    coding_phrases = [
        "create a python program",
        "write a python program",
        "make a python program",
        "build a python program",
        "create python code",
        "write python code",
        "make python code",
        "generate python code",
        "code this",
        "create code",
        "write code",
        "build code",
    ]

    if any(
        phrase in command
        for phrase in coding_phrases
    ):

        current_task = "CODING"

        # Remove common command words
        request = command

        for phrase in coding_phrases:

            if phrase in request:

                request = request.replace(
                    phrase,
                    "",
                    1
                ).strip()

                break

        if not request:

            return "What Python program should I create?"

        file_path = (
            r"E:\FridayAI\tests\archon_generated.py"
        )

        return build_python_project(
            request,
            file_path
        )

    # -------------------------
    # YouTube play
    # -------------------------

    if (
        "play youtube" in command
        or "play video" in command
    ):

        current_task = "YOUTUBE"

        # Search first using the words after "play"
        query = command.replace("play youtube", "", 1).strip()

        if not query:
            query = command.replace("play video", "", 1).strip()

        if not query:
            return "What YouTube video should I play?"

        search_result = search_youtube(query)

        if search_result.startswith("YouTube search failed"):
            return search_result

        import time
        time.sleep(4)

        return play_first_youtube_result()

    # -------------------------
    # YouTube search
    # -------------------------

    if command.startswith("search youtube "):

        query = command.replace(
            "search youtube ",
            "",
            1
        ).strip()

        if query:

            current_task = "YOUTUBE"
            current_page_active = False
            current_page_topic = query

            return search_youtube(query)

        return "What should I search for on YouTube?"
    

    # -------------------------
    # Google search
    # -------------------------

    if command.startswith("search "):

        query = command.replace("search ", "", 1).strip()

        if query:

            current_task = "BROWSER"
            current_page_active = True
            current_page_topic = query

            search_result = search_google(query)

            if search_result.startswith("Search failed"):
                return search_result

            import time
            time.sleep(3)

            page_text = get_current_page_text()

            if page_text.startswith("ERROR:"):
                return search_result

            if not page_text.strip():
                return search_result

            return ask_about_page(
                f"What is the answer to my search for {query}?",
                page_text
            )

        return "What should I search for?"

    # -------------------------
    # Page summary
    # -------------------------

    if (
        "summarize this page" in command
        or "summarise this page" in command
    ):

        page_text = get_current_page_text()

        if page_text.startswith("ERROR:"):
            return page_text

        if not page_text.strip():
            return "I couldn't find any text on the current page."

        return summarize_text(page_text)

    # -------------------------
    # Questions about current page
    # -------------------------

    if (
        "what is this page about" in command
        or "what this page about" in command
        or "ask about this page" in command
        or "question about this page" in command
    ):

        page_text = get_current_page_text()

        if page_text.startswith("ERROR:"):
            return page_text

        if not page_text.strip():
            return "I couldn't find any text on the current page."

        return ask_about_page(command, page_text)

    # -------------------------
    # Natural follow-up question about active webpage
    # -------------------------

    page_reference_words = [
        "it",
        "this",
        "that",
        "they",
        "them",
        "its",
        "their",
        "the page",
        "this page",
        "the website",
        "this website",
        "this universe",
        "this topic"
    ]

    is_page_followup = any(
        word in command
        for word in page_reference_words
    )

    if is_related_to_page(command):
        is_page_followup = True

    if current_page_active and is_page_followup:

        current_task = "WEBPAGE"

        page_text = get_current_page_text()

        if page_text.startswith("ERROR:"):
            return page_text

        if not page_text.strip():
            return None

        return ask_about_page(command, page_text)

    # Nothing matched
    return None