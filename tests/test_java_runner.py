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

from automation.vscode_controller import run_java_file


java_file = r"E:\FridayAI\tests\ArchonHello.java"

java_code = """public class ArchonHello {
    public static void main(String[] args) {
        System.out.println("HELLO FROM ARCHON JAVA");
    }
}
"""

with open(
    java_file,
    "w",
    encoding="utf-8"
) as f:
    f.write(java_code)


print(run_java_file(java_file))