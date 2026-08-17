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

from automation.vscode_extensions import (
    check_vscode,
    get_installed_extensions,
)


print("=== ARCHON VS CODE TEST ===")

installed, result = check_vscode()

if installed:
    print("VS CODE: INSTALLED")
    print("COMMAND:", result)

else:
    print("VS CODE: NOT AVAILABLE")
    print(result)

print()
print("=== INSTALLED EXTENSIONS ===")

extensions = get_installed_extensions()

if extensions:
    for extension in extensions:
        print(extension)
else:
    print("No extensions detected.")