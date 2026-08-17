import os
import shutil
import subprocess

from automation.vscode_extensions import (
    is_extension_installed,
    install_extension,
)


# =========================================================
# BASIC LANGUAGE REQUIREMENTS
# =========================================================

LANGUAGE_REQUIREMENTS = {

    "python": {
        "runtime": "python",
        "compiler": None,
        "extensions": [
            "ms-python.python",
        ],
    },

    "java": {
        "runtime": "java",
        "compiler": "javac",
        "extensions": [
            "vscjava.vscode-java-pack",
        ],
    },

    "javascript": {
        "runtime": "node",
        "compiler": None,
        "extensions": [],
    },

    "cpp": {
        "runtime": "g++",
        "compiler": None,
        "extensions": [
            "ms-vscode.cpptools",
        ],
    },
}


# =========================================================
# COMMAND CHECK
# =========================================================

def command_exists(command):

    if not command:
        return False

    return shutil.which(command) is not None


# =========================================================
# VERSION CHECK
# =========================================================

def get_version(command):

    if not command:
        return None

    try:

        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:

            output = (
                result.stdout.strip()
                or result.stderr.strip()
            )

            return output

        return None

    except Exception:

        return None


# =========================================================
# CHECK NODE.JS
# =========================================================

def check_node():

    node_path = shutil.which(
        "node"
    )

    # Windows PowerShell can block npm.ps1.
    # npm.cmd is therefore preferred.
    if os.name == "nt":

        npm_path = shutil.which(
            "npm.cmd"
        )

    else:

        npm_path = shutil.which(
            "npm"
        )

    node_installed = (
        node_path is not None
    )

    npm_installed = (
        npm_path is not None
    )

    node_version = None
    npm_version = None

    if node_installed:

        node_version = get_version(
            node_path
        )

    if npm_installed:

        npm_version = get_version(
            npm_path
        )

    return {
        "installed": (
            node_installed
            and npm_installed
        ),
        "node_path": node_path,
        "npm_path": npm_path,
        "node_version": node_version,
        "npm_version": npm_version,
    }


# =========================================================
# CHECK LANGUAGE
# =========================================================

def check_language(language):

    language = (
        language
        .lower()
        .strip()
    )

    # -----------------------------------------------------
    # Unknown language
    # -----------------------------------------------------

    if language not in LANGUAGE_REQUIREMENTS:

        return {
            "language": language,
            "ready": False,
            "runtime": None,
            "runtime_ready": False,
            "compiler": None,
            "compiler_ready": False,
            "missing_extensions": [],
            "message": (
                "Language is not in the basic "
                "runtime manager."
            ),
        }

    requirements = (
        LANGUAGE_REQUIREMENTS[
            language
        ]
    )

    runtime = requirements.get(
        "runtime"
    )

    compiler = requirements.get(
        "compiler"
    )

    # -----------------------------------------------------
    # Runtime
    # -----------------------------------------------------

    runtime_ready = True

    if runtime:

        runtime_ready = command_exists(
            runtime
        )

    # -----------------------------------------------------
    # Compiler
    # -----------------------------------------------------

    compiler_ready = True

    if compiler:

        compiler_ready = command_exists(
            compiler
        )

    # -----------------------------------------------------
    # VS Code extensions
    # -----------------------------------------------------

    missing_extensions = []

    for extension in requirements.get(
        "extensions",
        []
    ):

        if not is_extension_installed(
            extension
        ):

            missing_extensions.append(
                extension
            )

    # -----------------------------------------------------
    # Ready
    # -----------------------------------------------------

    ready = (
        runtime_ready
        and compiler_ready
        and not missing_extensions
    )

    return {
        "language": language,
        "runtime": runtime,
        "runtime_ready": runtime_ready,
        "compiler": compiler,
        "compiler_ready": compiler_ready,
        "missing_extensions": (
            missing_extensions
        ),
        "ready": ready,
    }


# =========================================================
# PREPARE LANGUAGE
# =========================================================

def prepare_language(language):

    result = check_language(
        language
    )

    # Already ready
    if result["ready"]:

        return result

    # -----------------------------------------------------
    # Install missing VS Code extensions
    # -----------------------------------------------------

    for extension in result.get(
        "missing_extensions",
        []
    ):

        print(
            "📦 ARCHON installing VS Code "
            f"extension: {extension}"
        )

        install_result = (
            install_extension(
                extension
            )
        )

        if (
            "installed"
            not in install_result.lower()
            and
            "already"
            not in install_result.lower()
        ):

            return {
                **result,
                "ready": False,
                "message": install_result,
            }

    # -----------------------------------------------------
    # Check again
    # -----------------------------------------------------

    result = check_language(
        language
    )

    return result