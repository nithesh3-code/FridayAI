from core.language_discovery import (
    discover_language,
)


print("=" * 50)
print("       ARCHON LANGUAGE DISCOVERY TEST")
print("=" * 50)


languages = [
    "python",
    "java",
    "javascript",
    "rust",
    "go",
    "cobra",
]


for language in languages:

    print()
    print(
        f"DISCOVERING: {language}"
    )

    result = discover_language(
        language
    )

    print(
        result
    )