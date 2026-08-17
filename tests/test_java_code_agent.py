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
print("        ARCHON JAVA CODE TEST")
print("========================================")

result = build_python_project(
    "Create a Java program that prints HELLO FROM ARCHON JAVA.",
    r"E:\FridayAI\tests\archon_java_test.java"
)

print()
print(result)