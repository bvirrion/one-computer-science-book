"""aslr.py -- where the stack and the code are, in five runs of one program: with
address-space layout randomisation, as programs normally run, then with it turned
off for the process (setarch -R), as the chapter's captured outputs run. Addresses
are printed in decimal."""

import subprocess
import tempfile
from pathlib import Path

C = r"""
#include <stdio.h>
int main(void) {
    char name[16];
    printf("%lu %lu\n", (unsigned long)name, (unsigned long)main);
    return 0;
}
"""
with tempfile.TemporaryDirectory() as d:
    src, exe = Path(d) / "where.c", Path(d) / "where"
    src.write_text(C)
    subprocess.run(["gcc", "-O0", "-o", exe, src], check=True)
    for label, cmd in (("randomised", [exe]), ("setarch -R", ["setarch", "-R", exe])):
        print(label + ":")
        for _ in range(5):
            out = subprocess.run(cmd, capture_output=True, text=True).stdout
            stack, code = map(int, out.split())
            print(f"  name at {stack:>19,}  main at {code:>19,}", end="")
            print(f"  main % 4096 = {code % 4096}")
