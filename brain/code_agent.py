import os
import re

from brain.ai import generate_ai_code

from automation.vscode_controller import (
    create_file,
)

from core.code_repair import (
    repair_code,
)

from automation.execution_manager import (
    execute_file,
)

from core.language_registry import (
    detect_language as registry_detect_language,
    get_language,
)

from core.language_discovery import (
    discover_language,
)

from core.environment_manager import (
    check_language,
)

# =========================================================
# LANGUAGE DETECTION
# =========================================================

def detect_language(request):

    return registry_detect_language(
        request
    )

# =========================================================
# CODE GENERATION
# =========================================================

def generate_code(request, language):

    prompt = f"""
You are ARCHON's professional coding agent.

Programming language:
{language}

User request:
{request}

Generate complete working source code.

Rules:
- Return ONLY source code.
- Do NOT use Markdown.
- Do NOT use ``` blocks.
- Do NOT explain the code.
- Make the code valid for {language}.
- Make the program directly runnable.
- Use the correct syntax and standard conventions for {language}.
"""

    try:

        code = generate_ai_code(prompt)

        return code.strip()

    except Exception as e:

        return f"CODE GENERATION ERROR: {e}"


# =========================================================
# JAVA CLASS NAME FIX
# =========================================================

def fix_java_class_name(code, file_path):

    class_name = os.path.splitext(
        os.path.basename(file_path)
    )[0]

    pattern = r"public\s+class\s+\w+"

    replacement = (
        f"public class {class_name}"
    )

    fixed_code, count = re.subn(
        pattern,
        replacement,
        code,
        count=1
    )

    return fixed_code


# =========================================================
# ENVIRONMENT CHECK
# =========================================================

def check_environment(language):

    print(
        f"🔍 ARCHON checking "
        f"{language} environment..."
    )

    result = check_language(
        language
    )

    if result.get("ready"):

        print(
            f"✅ {language} environment ready."
        )

        return None

    # -----------------------------------------------------
    # Runtime missing
    # -----------------------------------------------------

    if not result.get(
        "runtime_ready",
        True
    ):

        runtime = result.get(
            "runtime",
            "required runtime"
        )

        return (
            f"{language.upper()} "
            "ENVIRONMENT NOT READY\n"
            f"{runtime} is not installed "
            "or not available in PATH."
        )

    # -----------------------------------------------------
    # Compiler missing
    # -----------------------------------------------------

    if result.get("compiler"):

        if not result.get(
            "compiler_ready",
            True
        ):

            compiler = result.get(
                "compiler"
            )

            return (
                f"{language.upper()} "
                "ENVIRONMENT NOT READY\n"
                f"{compiler} is not installed "
                "or not available in PATH."
            )

    # -----------------------------------------------------
    # VS Code extensions missing
    # -----------------------------------------------------

    missing_extensions = result.get(
        "missing_extensions",
        []
    )

    if missing_extensions:

        return (
            f"{language.upper()} "
            "ENVIRONMENT NOT READY\n"
            "Missing VS Code extensions:\n"
            + "\n".join(
                missing_extensions
            )
        )

    return (
        f"{language.upper()} "
        "environment is not ready."
    )


# =========================================================
# BUILD PROJECT
# =========================================================

def build_project(
    request,
    file_path=None
):

    # -----------------------------------------------------
    # Detect language using registry
    # -----------------------------------------------------

    language = detect_language(
        request
    )

    # -----------------------------------------------------
    # Get language configuration from registry
    # -----------------------------------------------------

    config = get_language(
        language
    )

    if config is None:

        return (
            "=== ARCHON LANGUAGE RESULT ===\n"
            f"LANGUAGE: {language}\n"
            "Language discovery failed."
        )

    extension = config.get(
        "extension",
        ".txt"
    )

    # -----------------------------------------------------
    # Check environment
    # -----------------------------------------------------

    environment_error = (
        check_environment(
            language
        )
    )

    if environment_error:

        return (
            "=== ARCHON ENVIRONMENT RESULT ===\n"
            f"LANGUAGE: {language}\n"
            f"{environment_error}"
        )

    # -----------------------------------------------------
    # File path
    # -----------------------------------------------------

    if file_path is None:

        file_path = os.path.join(
            r"E:\FridayAI\tests",
            "archon_generated"
            + extension
        )

    else:

        base, _ = os.path.splitext(
            file_path
        )

        file_path = (
            base
            + extension
        )

    # -----------------------------------------------------
    # Generate code
    # -----------------------------------------------------

    print(
        f"🧠 ARCHON generating "
        f"{language} code..."
    )

    code = generate_code(
        request,
        language
    )

    if code.startswith(
        "CODE GENERATION ERROR:"
    ):

        return code

    # -----------------------------------------------------
    # Java class name correction
    # -----------------------------------------------------

    if language == "java":

        code = fix_java_class_name(
            code,
            file_path
        )

    # -----------------------------------------------------
    # Create source file
    # -----------------------------------------------------

    print(
        "📝 ARCHON creating file..."
    )

    create_result = create_file(
        file_path,
        code
    )

    if create_result.startswith(
        "Failed"
    ):

        return create_result

    # -----------------------------------------------------
    # Run program
    # -----------------------------------------------------

    print(
        f"▶️ ARCHON running "
        f"{language} code..."
    )

    # -----------------------------------------------------
    # Execute generated program
    # -----------------------------------------------------

    print(
        f"▶️ ARCHON executing "
        f"{language}..."
    )

    # DEBUG
    print("DEBUG LANGUAGE:", language)
    print("DEBUG CONFIG:", get_language(language))

    run_result = execute_file(
        language,
        file_path
    )
    # -----------------------------------------------------
    # AUTOMATIC CODE REPAIR
    # -----------------------------------------------------

    if (
        "FAILED" in run_result
        or "ERROR" in run_result
    ):

        print(
            "🔧 ARCHON detected execution failure."
        )

        print(
            "🧠 ARCHON analyzing the error..."
        )

        repaired_code = repair_code(
            language,
            code,
            run_result
        )

        if repaired_code:

            print(
                "📝 ARCHON writing repaired code..."
            )

            create_result = create_file(
                file_path,
                repaired_code
            )

            if not create_result.startswith(
                "Failed"
            ):

                code = repaired_code

                print(
                    "🔄 ARCHON retrying execution..."
                )

                run_result = execute_file(
                    language,
                    file_path
                )

    # -----------------------------------------------------
    # Final result
    # -----------------------------------------------------

    return (
        "=== ARCHON CODE RESULT ===\n"
        f"LANGUAGE: {language}\n"
        f"FILE: {file_path}\n"
        f"{run_result}"
    )