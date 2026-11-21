"""Ours against the shared package, on every program of the toy machine's chapter."""
import sys
from pathlib import Path

from assembler_m2 import assemble
from simulator_m4 import new_machine, run

CODE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(CODE / "shared" / "toymachine"))
import toymachine

PROGRAMS = CODE / "grade-11" / "02-von-neumann-machine" / "listings"
for path in sorted(PROGRAMS.glob("*.toy")):
    text = path.read_text()
    stdin = path.with_suffix(".stdin")
    inputs = [int(v, 0) for v in stdin.read_text().split()] if stdin.exists() else []
    ours = new_machine(assemble(text), inputs)
    theirs = toymachine.Machine(toymachine.assemble(text), inputs)
    run(ours)
    theirs.run()
    same = (ours["outputs"] == theirs.outputs
            and ours["mem"] == theirs.mem and ours["reg"] == theirs.reg
            and ours["flags"] == theirs.flags and ours["steps"] == theirs.steps
            and ours["sp"] == theirs.sp and ours["pc"] == theirs.pc)
    print(f"{path.name:<20} bytes {assemble(text) == toymachine.assemble(text)!s:<5}"
          f" outputs {str(ours['outputs']):<14} same outputs and state: {same}")
