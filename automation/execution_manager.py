import os
import shutil
import subprocess
import tempfile

from core.language_registry import get_language


# =========================================================
# COMMAND HELPERS
# =========================================================

def command_exists(command):

    if not command:
        return False

    return shutil.which(command) is not None


def run_command(
    command,
    args,
    cwd=None,
    timeout=30
):

    try:

        result = subprocess.run(
            [command, *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode == 0:

            return {
                "success": True,
                "output": output,
                "error": error
            }

        return {
            "success": False,
            "output": output,
            "error": error
        }

    except FileNotFoundError:

        return {
            "success": False,
            "output": "",
            "error": (
                f"Runtime not found: {command}"
            )
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "output": "",
            "error": (
                f"Execution timed out: {command}"
            )
        }

    except Exception as e:

        return {
            "success": False,
            "output": "",
            "error": str(e)
        }


# =========================================================
# RUNTIME EXECUTION
# =========================================================

def execute_runtime(
    config,
    file_path
):

    command = config.get(
        "run_command"
    )

    if not command:

        return (
            "EXECUTION FAILED\n"
            "No runtime command configured."
        )

    if not command_exists(command):

        return (
            "EXECUTION FAILED\n"
            f"Runtime not found: {command}"
        )

    result = run_command(
        command,
        [file_path]
    )

    if result["success"]:

        return (
            "PROGRAM RAN SUCCESSFULLY\n"
            + result["output"]
        )

    return (
        "EXECUTION FAILED\n"
        + result["error"]
    )


# =========================================================
# COMPILED EXECUTION
# =========================================================

def execute_compiled(
    config,
    file_path
):

    compiler = config.get(
        "compile_command"
    )

    runtime = config.get(
        "run_command"
    )

    if not compiler:

        return (
            "COMPILATION FAILED\n"
            "No compiler configured."
        )

    if not command_exists(compiler):

        return (
            "COMPILATION FAILED\n"
            f"Compiler not found: {compiler}"
        )

    source_dir = os.path.dirname(
        os.path.abspath(file_path)
    )

    source_name = os.path.basename(
        file_path
    )

    base_name = os.path.splitext(
        source_name
    )[0]

    # -----------------------------------------------------
    # Compile
    #
    # Do NOT assume "-o".
    # Compiler receives the source file directly.
    # -----------------------------------------------------

    compile_result = run_command(
        compiler,
        [source_name],
        cwd=source_dir
    )

    if not compile_result["success"]:

        return (
            "COMPILATION FAILED\n"
            + compile_result["error"]
        )

    # -----------------------------------------------------
    # Some compiled languages need a runtime command.
    # -----------------------------------------------------

    if runtime:

        if not command_exists(runtime):

            return (
                "EXECUTION FAILED\n"
                f"Runtime not found: {runtime}"
            )

        # Java-style execution:
        # javac Main.java
        # java Main
        #
        # The compiled program is identified by
        # the source filename without extension.

        result = run_command(
            runtime,
            [base_name],
            cwd=source_dir
        )

        if result["success"]:

            return (
                "PROGRAM RAN SUCCESSFULLY\n"
                + result["output"]
            )

        return (
            "EXECUTION FAILED\n"
            + result["error"]
        )

    # -----------------------------------------------------
    # No runtime command.
    #
    # Compilation itself is considered successful.
    # -----------------------------------------------------

    return (
        "COMPILATION SUCCESSFUL\n"
        f"Source: {file_path}"
    )


# =========================================================
# EXECUTE FILE
# =========================================================

def execute_file(
    language,
    file_path
):

    language = language.lower().strip()

    # -----------------------------------------------------
    # File check
    # -----------------------------------------------------

    if not os.path.exists(file_path):

        return (
            "EXECUTION FAILED\n"
            f"File does not exist: {file_path}"
        )

    # -----------------------------------------------------
    # Registry lookup
    # -----------------------------------------------------

    config = get_language(
        language
    )

    if config is None:

        return (
            "EXECUTION NOT SUPPORTED\n"
            f"Language: {language}"
        )

    execution_type = config.get(
        "execution_type",
        "unknown"
    )

    # -----------------------------------------------------
    # Runtime
    # -----------------------------------------------------

    if execution_type == "runtime":

        return execute_runtime(
            config,
            file_path
        )

    # -----------------------------------------------------
    # Compiled
    # -----------------------------------------------------

    if execution_type == "compiled":

        return execute_compiled(
            config,
            file_path
        )

    # -----------------------------------------------------
    # Browser
    # -----------------------------------------------------

    if execution_type == "browser":

        return (
            "BROWSER EXECUTION NOT "
            "IMPLEMENTED YET\n"
            f"Language: {language}"
        )

    # -----------------------------------------------------
    # Unknown
    # -----------------------------------------------------

    return (
        "EXECUTION NOT SUPPORTED\n"
        f"Language: {language}\n"
        "Execution type is unknown."
    )


# =========================================================
# SUPPORT CHECK
# =========================================================

def is_execution_supported(
    language
):

    language = language.lower().strip()

    config = get_language(
        language
    )

    if config is None:

        return False

    execution_type = config.get(
        "execution_type",
        "unknown"
    )

    return execution_type in {
        "runtime",
        "compiled",
        "browser"
    }


# =========================================================
# DISCOVERED EXECUTORS
# =========================================================

def get_supported_executors():

    # IMPORTANT:
    # No hardcoded language list.
    #
    # The registry is the source of truth.

    from core.language_registry import (
        load_registry
    )

    registry = load_registry()

    supported = []

    for language, config in registry.items():

        execution_type = config.get(
            "execution_type",
            "unknown"
        )

        if execution_type in {
            "runtime",
            "compiled",
            "browser"
        }:

            supported.append(
                language
            )

    return supported