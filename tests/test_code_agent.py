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

from brain.code_agent import build_python_project


print("========================================")
print("        ARCHON CODE AGENT TEST")
print("========================================")

result = build_python_project(
    "Create a Python program that prints Hello from ARCHON.",
    r"E:\FridayAI\tests\generated_archon.py"
)

print()
print("=== ARCHON CODE RESULT ===")
print(result)