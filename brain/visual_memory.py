# ARCHON Visual Conversation Memory

_visual_history = []


def add_visual_message(role, content):
    """
    Store a visual conversation message.
    
    role:
        user
        assistant
    """

    _visual_history.append({
        "role": role,
        "content": content
    })


def get_visual_history():
    """
    Return the current visual conversation history.
    """

    return list(_visual_history)


def clear_visual_memory():
    """
    Clear visual conversation memory.
    """

    _visual_history.clear()