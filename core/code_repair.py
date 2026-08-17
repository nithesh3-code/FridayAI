from brain.ai import ask_ai


# =========================================================
# CLEAN GENERATED CODE
# =========================================================

def clean_code(text):

    if not text:
        return ""

    text = text.strip()

    # Remove accidental Markdown fences
    if text.startswith("```"):

        lines = text.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines)

    return text.strip()


# =========================================================
# REPAIR CODE
# =========================================================

def repair_code(
    language,
    code,
    error
):

    prompt = f"""
You are ARCHON's automatic code repair engine.

Programming language:
{language}

SOURCE CODE:
{code}

EXECUTION / COMPILATION ERROR:
{error}

Your task:

1. Find the actual cause of the error.
2. Correct the source code.
3. Preserve the user's original intent.
4. Do not unnecessarily rewrite working code.
5. Return the COMPLETE corrected source code.

STRICT OUTPUT RULES:

- Return ONLY source code.
- Do NOT use Markdown.
- Do NOT use ``` blocks.
- Do NOT explain anything.
- Do NOT include comments outside the source code.
- The result must be directly runnable/compilable.
"""

    try:

        response = ask_ai(
            prompt
        )

        return clean_code(
            response
        )

    except Exception:

        return ""