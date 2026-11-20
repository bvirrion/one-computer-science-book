import io
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CODE = HERE.parents[1]
for p in (HERE / "listings", HERE / "exercises", CODE / "shared" / "toymachine"):
    sys.path.insert(0, str(p))

import simulator_m3  # noqa: E402
import simulator_m4  # noqa: E402
import toy_ex  # noqa: E402
import toymachine  # noqa: E402
from assembler_m2 import assemble  # noqa: E402
from toymachine.__main__ import main as shared_tool  # noqa: E402
from trace_m5 import disassemble, run_traced  # noqa: E402

PROGRAMS = sorted((CODE / "grade-11" / "02-von-neumann-machine" / "listings").glob("*.toy"))


def inputs_of(path):
    stdin = path.with_suffix(".stdin")
    return [int(v, 0) for v in stdin.read_text().split()] if stdin.exists() else []


def test_traces_identical_to_shared_tool():
    for path in PROGRAMS:
        ours, theirs = io.StringIO(), io.StringIO()
        with redirect_stdout(ours):
            run_traced(simulator_m4.new_machine(assemble(path.read_text()), inputs_of(path)),
                       simulator_m4.run)
        old = sys.stdin
        sys.stdin = io.StringIO("\n".join(str(v) for v in inputs_of(path)) + "\n")
        try:
            with redirect_stdout(theirs):
                shared_tool(["run", "--trace", str(path)])
        finally:
            sys.stdin = old
        assert ours.getvalue() == theirs.getvalue(), path.name


def test_random_programs_same_state():
    rng = random.Random(10)
    for _ in range(300):
        memory = [rng.randrange(256) for _ in range(256)]
        for a in range(0, 64, 2):                       # valid opcodes in the first words
            memory[a] = 4 * rng.randrange(28) + rng.randrange(4)
        ours = simulator_m4.new_machine(memory, [rng.randrange(256) for _ in range(50)])
        theirs = toymachine.Machine(memory, list(ours["inputs"]))
        for _ in range(40):
            if theirs.halted:
                break
            try:
                theirs.step()
            except toymachine.ToyError:
                break
            simulator_m3.step(ours, simulator_m4.EXECUTE)
            assert (ours["reg"], ours["pc"], ours["sp"], ours["flags"], ours["mem"]) == \
                   (theirs.reg, theirs.pc, theirs.sp, theirs.flags, theirs.mem)


def test_disassembly_and_counts():
    for b0 in range(4 * 28):
        for b1 in range(256):
            assert disassemble(b0, b1) == toymachine.disassemble(b0, b1)
    assert toy_ex.count_instructions() == 5791


def test_exercises():
    assert [toy_ex.parse_number(t) for t in ["42", "0x2A", "0b101010", "'*'", "-3"]] == \
        [42, 42, 42, 42, 253]
    for v in range(256):
        for name, fn in (("NOT", toy_ex.not_), ("SHR", toy_ex.shr)):
            text = f"LOADI R0, {v}\n{name} R0\nHALT"
            m = simulator_m4.new_machine(assemble(text))
            simulator_m4.run(m)
            mine = simulator_m4.new_machine(assemble(text))
            simulator_m4.step(mine)
            fn(mine, 0, 0)
            assert (mine["reg"], mine["flags"]) == (m["reg"], m["flags"])
    text = "INC R1\nINC R1\nOUT R1\nHALT"
    assert toy_ex.assemble_with_inc(text) == assemble(text.replace("INC R1", "ADDI R1, 1"))
    sum_array = PROGRAMS[-1]
    m = simulator_m4.new_machine(assemble(sum_array.read_text()))
    simulator_m4.run(m)
    tool = io.StringIO()
    with redirect_stdout(tool):
        shared_tool(["run", "--dump", str(sum_array)])
    assert tool.getvalue().endswith(toy_ex.dump(m) + "\n")
    max2 = next(p for p in PROGRAMS if p.name == "max2.toy")
    bad = simulator_m4.new_machine(assemble(max2.read_text()), [57, 201])
    simulator_m3.run(bad, 100, toy_ex.inverted_borrow())
    assert bad["outputs"] == [57]
