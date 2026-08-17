import json
import os
import re

from brain.ai import ask_ai


# =========================================================
# CONFIGURATION
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
# SAVE REGISTRY
# =========================================================

def save_registry(registry):

    with open(
        REGISTRY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            registry,
            file,
            indent=4
        )


# =========================================================
# NORMALIZE AI JSON
# =========================================================

def extract_json(text):

    text = text.strip()

    # Remove markdown fences if AI accidentally adds them
    text = re.sub(
        r"^```(?:json)?",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```$",
        "",
        text
    )

    text = text.strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:

        raise ValueError(
            "AI did not return valid JSON."
        )

    return json.loads(
        text[start:end + 1]
    )


# =========================================================
# DISCOVER LANGUAGE
# =========================================================

def discover_language(request):

    request = request.lower().strip()

    language = request

    registry = load_registry()

    # -----------------------------------------------------
    # Already discovered
    # -----------------------------------------------------

    if language in registry:

        return registry[language]


    # -----------------------------------------------------
    # Ask ARCHON AI
    # -----------------------------------------------------

    prompt = f"""
You are ARCHON's programming-language discovery engine.

Identify the programming language from this user request:

{request}

Return ONLY valid JSON.

Do not use Markdown.
Do not use code fences.
Do not explain anything.

Required JSON structure:

{{
    "language": "canonical language name",
    "aliases": [],
    "extension": ".ext",
    "runtime": null,
    "compiler": null,
    "vscode_extensions": [],
    "execution_type": "runtime",
    "run_command": null,
    "compile_command": null,
    "confidence": 0.0
}}

Rules:

1. extension must include the dot.
2. runtime is the executable normally used to run the language,
   or null if compilation is required.
3. compiler is the compiler executable,
   or null if not required.
4. vscode_extensions must contain known VS Code Marketplace
   extension IDs when one is known.
5. execution_type must be one of:
   "runtime"
   "compiled"
   "browser"
   "unknown"
6. run_command must be the executable name only,
   for example:
   "python"
   "node"
   "ruby"
   "php"

7. compile_command must be the compiler executable only,
   for example:
   "javac"
   "g++"
   "rustc"

8. Never invent a runtime or compiler.
9. If you are not confident, use null.
10. confidence must be between 0 and 1.
"""

    try:

        response = ask_ai(
            prompt
        )

        config = extract_json(
            response
        )

    except Exception as e:

        return {
            "language": language,
            "error": (
                f"Language discovery failed: {e}"
            )
        }


    # =====================================================
    # VALIDATE
    # =====================================================

    if not isinstance(
        config,
        dict
    ):

        return {
            "language": language,
            "error": "Invalid language configuration."
        }


    config["language"] = (
        config.get(
            "language",
            language
        )
        .lower()
        .strip()
    )

    config.setdefault(
        "aliases",
        []
    )

    config.setdefault(
        "extension",
        None
    )

    config.setdefault(
        "runtime",
        None
    )

    config.setdefault(
        "compiler",
        None
    )

    config.setdefault(
        "vscode_extensions",
        []
    )

    config.setdefault(
        "execution_type",
        "unknown"
    )

    config.setdefault(
        "run_command",
        None
    )

    config.setdefault(
        "compile_command",
        None
    )

    config.setdefault(
        "confidence",
        0
    )


    # =====================================================
    # LOW CONFIDENCE
    # =====================================================

    try:

        confidence = float(
            config["confidence"]
        )

    except Exception:

        confidence = 0


    if confidence < 0.70:

        config["discovery_status"] = (
            "LOW_CONFIDENCE"
        )

        return config


    # =====================================================
    # SAVE DISCOVERED LANGUAGE
    # =====================================================

    registry[
        config["language"]
    ] = config

    save_registry(
        registry
    )

    config["discovery_status"] = (
        "DISCOVERED"
    )

    return config