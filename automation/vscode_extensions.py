import subprocess
import shutil


def get_code_command():
    """
    Find the VS Code command.
    """
    code = shutil.which("code")

    if code:
        return code

    # Windows commonly exposes VS Code through code.cmd
    code_cmd = shutil.which("code.cmd")

    if code_cmd:
        return code_cmd

    return None


def check_vscode():
    """
    Check whether VS Code command is available.
    """
    code = get_code_command()

    if not code:
        return False, "VS Code command not found."

    return True, code


def get_installed_extensions():
    """
    Return installed VS Code extensions.
    """
    code = get_code_command()

    if not code:
        return []

    try:
        result = subprocess.run(
            [code, "--list-extensions"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return []

        return [
            extension.strip().lower()
            for extension in result.stdout.splitlines()
            if extension.strip()
        ]

    except Exception:
        return []


def is_extension_installed(extension_id):
    """
    Check whether a specific VS Code extension is installed.
    """
    extensions = get_installed_extensions()

    return extension_id.lower() in extensions


def install_extension(extension_id):
    """
    Install a VS Code extension if it is missing.
    """
    code = get_code_command()

    if not code:
        return "VS Code command not found."

    if is_extension_installed(extension_id):
        return (
            f"VS Code extension already installed: "
            f"{extension_id}"
        )

    try:
        result = subprocess.run(
            [
                code,
                "--install-extension",
                extension_id,
                "--force"
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            return (
                f"VS Code extension installed: "
                f"{extension_id}"
            )

        error = result.stderr.strip()

        return (
            f"Failed to install VS Code extension "
            f"{extension_id}: {error}"
        )

    except subprocess.TimeoutExpired:
        return (
            f"Extension installation timed out: "
            f"{extension_id}"
        )

    except Exception as e:
        return f"Extension installation error: {e}"


def ensure_extension(extension_id):
    """
    Make sure an extension exists.
    Install it when missing.
    """
    if is_extension_installed(extension_id):
        return (
            f"Extension ready: {extension_id}"
        )

    return install_extension(extension_id)