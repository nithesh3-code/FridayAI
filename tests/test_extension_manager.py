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
    is_extension_installed,
    ensure_extension,
)


print("=== ARCHON EXTENSION MANAGER TEST ===")

extensions_to_check = [
    "ms-python.python",
    "vscjava.vscode-java-pack",
    "ms-vscode.cpptools",
]


for extension in extensions_to_check:

    print()
    print("Checking:", extension)

    if is_extension_installed(extension):

        print("✅ Already installed")

    else:

        print("❌ Missing")
        print("ARCHON would install it.")

        # DO NOT install anything during this test.