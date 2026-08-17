from automation.execution_manager import (
    execute_file,
    get_supported_executors,
    is_execution_supported,
)


print("========================================")
print("       ARCHON EXECUTION MANAGER TEST")
print("========================================")
print()


print("SUPPORTED EXECUTORS:")

for language in get_supported_executors():
    print(f"✅ {language}")


print()
print("SUPPORT CHECK:")

for language in [
    "python",
    "java",
    "javascript",
    "rust",
]:
    print(
        f"{language}:",
        is_execution_supported(language)
    )


print()
print("========================================")
print("           PYTHON TEST")
print("========================================")

print(
    execute_file(
        "python",
        r"E:\FridayAI\tests\generated_archon.py"
    )
)


print()
print("========================================")
print("             JAVA TEST")
print("========================================")

print(
    execute_file(
        "java",
        r"E:\FridayAI\tests\archon_java_test.java"
    )
)


print()
print("========================================")
print("        JAVASCRIPT TEST")
print("========================================")


javascript_file = (
    r"E:\FridayAI\tests\execution_manager_test.js"
)

with open(
    javascript_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        'console.log("HELLO FROM ARCHON JAVASCRIPT");'
    )


print(
    execute_file(
        "javascript",
        javascript_file
    )
)