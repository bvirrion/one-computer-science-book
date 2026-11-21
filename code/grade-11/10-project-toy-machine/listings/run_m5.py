import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

from assembler_m2 import assemble
from simulator_m4 import new_machine, run
from trace_m5 import run_traced

CODE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(CODE / "shared" / "toymachine"))
from toymachine.__main__ import main as shared_tool

program = CODE / "grade-11" / "02-von-neumann-machine" / "listings" / "max2.toy"
ours, theirs = io.StringIO(), io.StringIO()
with redirect_stdout(ours):
    run_traced(new_machine(assemble(program.read_text()), [57, 201]), run)
sys.stdin = io.StringIO("57\n201\n")
with redirect_stdout(theirs):
    shared_tool(["run", "--trace", str(program)])
print(ours.getvalue(), end="")
print("same text as the shared tool:", ours.getvalue() == theirs.getvalue())
