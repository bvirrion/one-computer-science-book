"""A Python program starts another program, a child process, and waits for it."""
import subprocess
import sys

child = "import os; print('child: my parent is process', os.getppid() > 0); exit(3)"
result = subprocess.run([sys.executable, "-c", child], capture_output=True, text=True)
print("parent: the child printed:", result.stdout.strip())
print("parent: the child's exit status:", result.returncode)
result = subprocess.run(["ls", "no-such-file"], capture_output=True, text=True)
print("parent: ls exited with", result.returncode, "and wrote:", result.stderr.strip())
