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
print("       ARCHON NODE.JS CODE TEST")
print("========================================")

result = build_python_project(
    "Create a Node.js program that prints Hello from ARCHON.",
    r"E:\FridayAI\tests\archon_node_test.js"
)

print()
print(result)