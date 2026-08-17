import shutil
import subprocess


# =========================================================
# CHECK COMMAND
# =========================================================

def check_command(command):

    try:

        path = shutil.which(command)

        if path:
            return True, path

        return False, None

    except Exception:

        return False, None


# =========================================================
# GET VERSION
# =========================================================

def get_version(command):

    try:

        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )

        output = (
            result.stdout.strip()
            or result.stderr.strip()
        )

        return output

    except Exception as e:

        return f"ERROR: {e}"


# =========================================================
# CHECK PYTHON
# =========================================================

def check_python():

    exists, path = check_command("python")

    return {
        "name": "Python",
        "installed": exists,
        "path": path,
        "version": get_version("python")
        if exists else None
    }


# =========================================================
# CHECK JAVA
# =========================================================

def check_java():

    exists, path = check_command("java")

    return {
        "name": "Java",
        "installed": exists,
        "path": path,
        "version": get_version("java")
        if exists else None
    }


# =========================================================
# CHECK JAVAC
# =========================================================

def check_javac():

    exists, path = check_command("javac")

    return {
        "name": "Java Compiler",
        "installed": exists,
        "path": path,
        "version": get_version("javac")
        if exists else None
    }


# =========================================================
# CHECK NODE.JS
# =========================================================

def check_node():

    exists, path = check_command("node")

    return {
        "name": "Node.js",
        "installed": exists,
        "path": path,
        "version": get_version("node")
        if exists else None
    }


# =========================================================
# CHECK NPM
# =========================================================

def check_npm():

    exists, path = check_command("npm")

    return {
        "name": "npm",
        "installed": exists,
        "path": path,
        "version": get_version("npm")
        if exists else None
    }


# =========================================================
# CHECK GCC
# =========================================================

def check_gcc():

    exists, path = check_command("gcc")

    return {
        "name": "GCC",
        "installed": exists,
        "path": path,
        "version": get_version("gcc")
        if exists else None
    }


# =========================================================
# CHECK VS CODE
# =========================================================

def check_vscode():

    exists, path = check_command("code")

    return {
        "name": "VS Code",
        "installed": exists,
        "path": path,
        "version": get_version("code")
        if exists else None
    }


# =========================================================
# FULL ENVIRONMENT CHECK
# =========================================================

def check_environment():

    return {

        "python": check_python(),

        "java": check_java(),

        "javac": check_javac(),

        "node": check_node(),

        "npm": check_npm(),

        "gcc": check_gcc(),

        "vscode": check_vscode()

    }


# =========================================================
# PRINT ENVIRONMENT
# =========================================================

def print_environment():

    environment = check_environment()

    print()
    print("========================================")
    print("       ARCHON DEVELOPMENT ENVIRONMENT")
    print("========================================")
    print()

    for key, info in environment.items():

        if info["installed"]:

            print(
                f"✅ {info['name']}: INSTALLED"
            )

            print(
                f"   Path: {info['path']}"
            )

            if info["version"]:

                print(
                    f"   Version: {info['version']}"
                )

        else:

            print(
                f"❌ {info['name']}: NOT INSTALLED"
            )

        print()

    print("========================================")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print_environment()