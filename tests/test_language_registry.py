import sys
import os

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from core.language_registry import (
    detect_language,
    get_language,
)


tests = [
    "write a python program",
    "create java hello world",
    "make a node js program",
    "write javascript code",
    "create a c++ program",
    "write a rust program",
    "make a go program",
    "create a php program",
    "write a dart program",
    "make a typescript program",
]


print("========================================")
print("       ARCHON LANGUAGE REGISTRY")
print("========================================")

for request in tests:

    language = detect_language(request)
    config = get_language(language)

    print()
    print("REQUEST:", request)
    print("DETECTED:", language)
    print("FILE:", config["extension"])
    print("RUNTIME:", config["runtime"])
    print("COMPILER:", config["compiler"])