import json
import os


# =========================================================
# REGISTRY FILE
# =========================================================

REGISTRY_FILE = os.path.join(
    os.path.dirname(__file__),
    "language_registry.json"
)


# =========================================================
# LOAD REGISTRY
# =========================================================

def load_registry():

    if not os.path.exists(REGISTRY_FILE):
        return {}

    try:

        with open(
            REGISTRY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


# =========================================================
# GET LANGUAGE
# =========================================================

def get_language(language):

    language = language.lower().strip()

    registry = load_registry()

    return registry.get(language)


# =========================================================
# DETECT LANGUAGE
# =========================================================

def detect_language(text):

    text = text.lower()

    registry = load_registry()

    # Build alias list
    aliases = []

    for language, config in registry.items():

        aliases.append(
            (language, language)
        )

        for alias in config.get(
            "aliases",
            []
        ):

            aliases.append(
                (alias.lower(), language)
            )

    # Check longer aliases first
    aliases.sort(
        key=lambda item: len(item[0]),
        reverse=True
    )

    for alias, language in aliases:

        if alias in text:

            return language

    # Default ARCHON language
    return "python"