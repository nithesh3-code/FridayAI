import os
import base64
from brain.visual_memory import (
    add_visual_message,
    get_visual_history
)

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


VISION_MODEL = "qwen/qwen3.6-27b"


def encode_image(image_path):

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


def analyze_image(image_path, question="What is in this image?"):

    try:

        base64_image = encode_image(image_path)

        history = get_visual_history()

        messages = [
            {
                "role": "system",
                "content": (
                    "You are ARCHON Vision. "
                    "Answer questions about the supplied image. "
                    "Use only information that can reasonably be observed "
                    "in the image. Do not invent details. "
                    "Use the previous visual conversation when the user "
                    "uses words like 'it', 'this', 'that', 'he', 'she', "
                    "or other references to earlier visual information. "
                    "Keep answers clear and natural."
                )
            }
        ]

        # Add previous visual conversation
        messages.extend(history)

        # Add current image + question
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:image/jpeg;base64,"
                                f"{base64_image}"
                            )
                        }
                    }
                ]
            }
        )

        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=messages,
            max_completion_tokens=1024
        )

        answer = response.choices[0].message.content

        # Remove visible reasoning
        if "<think>" in answer:

            answer = answer.split(
                "<think>",
                1
            )[1]

            if "</think>" in answer:

                answer = answer.split(
                    "</think>",
                    1
                )[1]

        answer = answer.strip()

        # Save conversation
        add_visual_message(
            "user",
            question
        )

        add_visual_message(
            "assistant",
            answer
        )

        return answer

    except Exception as e:

        return f"Vision error: {e}"