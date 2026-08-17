import os
import re

from dotenv import load_dotenv
from groq import Groq

from memory.conversation import add_message, get_history


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -------------------------------------------------
# Clean AI output
# -------------------------------------------------

def clean_response(text):

    if not text:
        return ""

    # Remove hidden reasoning if the model returns it
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    # Remove accidental leading/trailing whitespace
    text = text.strip()

    return text

def wants_detailed_answer(prompt):

    detailed_words = [
        "in detail",
        "detailed",
        "deeply",
        "deep explanation",
        "full explanation",
        "explain fully",
        "explain in detail",
        "step by step",
        "step-by-step",
        "complete explanation",
        "everything about",
        "all about",
        "long explanation",
        "examples",
        "with examples"
    ]

    prompt = prompt.lower()

    return any(
        phrase in prompt
        for phrase in detailed_words
    )


def make_short_answer(text):

    text = clean_response(text)

    if not text:
        return ""

    # Remove markdown headings/bullets for simple spoken answers
    text = re.sub(r"[*#_`]", "", text)

    # Split into sentences
    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    # ARCHON default: maximum 2 sentences
    if len(sentences) > 2:
        sentences = sentences[:2]

    return " ".join(sentences)

# -------------------------------------------------
# Normal ARCHON AI
# -------------------------------------------------

def ask_ai(prompt):

    add_message("user", prompt)

    messages = [
        {
            "role": "system",
            "content": """
    You are ARCHON, a helpful personal AI assistant.

    Answer the user's actual question directly.

    DEFAULT MODE:
    - Give only the answer needed.
    - Keep the response to 1-2 sentences.
    - Do not provide lists unless the user asks for them.
    - Do not provide examples unless requested.
    - Do not add background information.
    - Do not ask "Would you like to know more?"
    - Do not repeat the question.
    - Never expose internal reasoning.
    - Never output <think>...</think>.

    DETAILED MODE:
    Only give a long explanation when the user explicitly asks for:
    "detailed", "in detail", "explain fully", "step by step",
    "deep explanation", "examples", or similar wording.

    Always answer the exact question first.
    """
        }
    ]

    history = get_history()

    # Only send the latest 6 messages to Groq
    messages.extend(history[-6:])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content

    reply = clean_response(reply)

    if not wants_detailed_answer(prompt):
        reply = make_short_answer(reply)

    add_message("assistant", reply)

    return reply


# -------------------------------------------------
# Webpage question answering
# -------------------------------------------------

def ask_about_page(question, page_text):

    prompt = f"""
You are ARCHON's webpage question-answering system.

The user is asking about the webpage currently open in Chrome.

Use ONLY the supplied webpage content.

Rules:

- Answer exactly the user's question.
- Do not use outside knowledge.
- Do not guess.
- Do not add unrelated information.
- If the answer cannot be found in the webpage, say exactly:
  "I couldn't find that information on this page."
- Simple questions: 1-3 sentences.
- Detailed questions: provide more detail.
- Do not expose internal reasoning.
- Never output <think>...</think>.
- Keep the answer natural and easy to speak aloud.

WEBPAGE CONTENT:

{page_text[:12000]}

USER QUESTION:

{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer questions strictly from the supplied "
                    "webpage content."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    reply = response.choices[0].message.content

    return clean_response(reply)


# -------------------------------------------------
# Webpage summary
# -------------------------------------------------

def summarize_text(text):

    prompt = f"""
You are ARCHON, a personal AI assistant.

Summarize the webpage below.

Rules:

- Give only the most important information.
- Use simple English.
- Maximum 5 points.
- Keep it concise.
- Do not add outside information.
- Do not expose internal reasoning.
- Never output <think>...</think>.

WEBPAGE:

{text[:12000]}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You summarize webpages clearly and concisely."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    reply = response.choices[0].message.content

    return clean_response(reply)