import json
import os

MEMORY_FILE = "memory/conversation.json"

conversation_history = []


def load_memory():
    global conversation_history

    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                conversation_history = json.load(file)
        except Exception:
            conversation_history = []


def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(conversation_history, file, indent=2, ensure_ascii=False)


def add_message(role, content):
    conversation_history.append({
        "role": role,
        "content": content
    })

    # Keep only latest 6 messages
    if len(conversation_history) > 6:
        conversation_history.pop(0)
        save_memory()


def get_history():
    return conversation_history

load_memory()