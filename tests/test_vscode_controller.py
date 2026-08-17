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

from brain.code_agent import generate_code


result = generate_code(
    "Create a simple Python program that prints Hello from ARCHON."
)

print("=== GENERATED CODE ===")
print(result)