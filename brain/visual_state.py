# ARCHON Visual State

current_image_path = None


def set_image(path):
    global current_image_path
    current_image_path = path


def get_image():
    return current_image_path


def clear_image():
    global current_image_path
    current_image_path = None