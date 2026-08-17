import shutil
import subprocess

from core.language_registry import get_language

from automation.runtime_manager import check_node


# =========================================================
# COMMAND HELPERS
# =========================================================

def command_exists(command):

    if not command:
        return True

    return shutil.which(command) is not None


def get_version(command):

    try:

        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:

            return result.stdout.strip()

        return None

    except Exception:

        return None


# =========================================================
# CHECK LANGUAGE ENVIRONMENT
# =========================================================

def check_language(language):

    language = language.lower().strip()

    config = get_language(language)

    # -----------------------------------------------------
    # Unknown language
    # -----------------------------------------------------

    if config is None:

        return {
            "language": language,
            "ready": False,
            "message": (
                f"ARCHON does not currently support "
                f"execution of {language}."
            ),
        }

    runtime = config.get("runtime")
    compiler = config.get("compiler")

    # -----------------------------------------------------
    # Runtime
    # -----------------------------------------------------

    runtime_ready = True
    runtime_version = None

    if runtime:

        # Special Node.js check
        if runtime == "node":

            node_info = check_node()

            runtime_ready = node_info.get(
                "installed",
                False
            )

            runtime_version = node_info.get(
                "node_version"
            )

        else:

            runtime_ready = command_exists(
                runtime
            )

            if runtime_ready:

                runtime_version = get_version(
                    runtime
                )

    # -----------------------------------------------------
    # Compiler
    # -----------------------------------------------------

    compiler_ready = True
    compiler_version = None

    if compiler:

        compiler_ready = command_exists(
            compiler
        )

        if compiler_ready:

            compiler_version = get_version(
                compiler
            )

    # -----------------------------------------------------
    # READY
    #
    # VS Code extensions are intentionally NOT checked.
    # -----------------------------------------------------

    ready = (
        runtime_ready
        and compiler_ready
    )

    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    return {

        "language": language,

        "extension": config.get(
            "extension"
        ),

        "runtime": runtime,

        "runtime_ready": runtime_ready,

        "runtime_version": runtime_version,

        "compiler": compiler,

        "compiler_ready": compiler_ready,

        "compiler_version": compiler_version,

        "execution_type": config.get(
            "execution_type"
        ),

        "run_command": config.get(
            "run_command"
        ),

        "compile_command": config.get(
            "compile_command"
        ),

        "ready": ready,
    }


# =========================================================
# PREPARE LANGUAGE
# =========================================================

def prepare_language(language):

    return check_language(language)