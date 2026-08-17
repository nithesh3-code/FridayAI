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

from core.environment_manager import (
    check_language,
)


print("========================================")
print("      ARCHON LANGUAGE ENVIRONMENT")
print("========================================")


for language in [
    "python",
    "java",
    "javascript",
    "cpp",
]:

    print()
    print("LANGUAGE:", language.upper())

    result = check_language(language)

    print("READY:", result["ready"])

    if "runtime_ready" in result:
        print(
            "RUNTIME:",
            "✅" if result["runtime_ready"] else "❌"
        )

    if result.get("compiler"):

        print(
            "COMPILER:",
            "✅" if result["compiler_ready"] else "❌"
        )

    missing = result.get(
        "missing_extensions",
        []
    )

    if missing:

        print(
            "MISSING EXTENSIONS:",
            ", ".join(missing)
        )

    else:

        print(
            "EXTENSIONS: ✅"
        )