"""cmd_inject.py -- the toy app prints a report title with the system's echo. With
shell=True the title is parsed by the shell, so a ';' starts a second command (here
a harmless second echo); with a list of arguments, no shell sees it."""

import subprocess

title = "Spring loans; echo SECOND COMMAND RAN"
print("shell=True:", flush=True)
subprocess.run(f"echo Report: {title}", shell=True)
print("list form:", flush=True)
subprocess.run(["echo", "Report:", title])
