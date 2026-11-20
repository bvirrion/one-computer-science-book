"""Grade 7, chapter 4: every toy program, run on the shared toy machine."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE.parent.parent / "shared" / "toymachine"))

from toymachine import Machine, assemble  # noqa: E402


def run(folder, name, inputs=(), steps=None):
    machine = Machine(assemble((HERE / folder / f"{name}.toy").read_text()), inputs=list(inputs))
    if steps is None:
        machine.run()
    else:
        for _ in range(steps):
            machine.step()
    return machine


def test_listings():
    m = run("listings", "add_two", [3, 4])
    assert m.outputs == [7] and m.steps == 5
    m = run("listings", "sum", [4])
    assert m.outputs == [10] and m.steps == 17
    assert run("listings", "countdown").outputs == [3, 2, 1]
    code = assemble((HERE / "listings" / "add_two.toy").read_text())
    assert code[:10] == [76, 0, 77, 0, 16, 1, 80, 0, 0, 0]


def test_sum_steps():
    for n in range(1, 11):
        m = run("listings", "sum", [n])
        assert m.outputs == [n * (n + 1) // 2] and m.steps == 3 * n + 5


def test_never_ends():
    m = run("listings", "never_ends", steps=10_000)
    assert m.outputs == [3] * 2000


def test_multiply():
    for b in range(1, 11):
        m = run("listings", "multiply", [6, b])
        assert m.outputs == [6 * b] and m.steps == 3 * b + 6
    assert run("listings", "multiply", [3, 50]).steps == 156
    assert run("listings", "multiply", [50, 3]).steps == 15
    assert run("listings", "multiply", [7, 200]).outputs == [1400 % 256]


def test_exercises():
    m = run("exercises", "three_steps")
    assert m.reg[:2] == [3, 2]
    m = run("listings", "sum", [4], steps=4)
    assert m.pc == 8
    assert run("exercises", "sum_plus_one", [3, 4]).outputs == [8]
    m = run("exercises", "no_halt", [3, 4])
    assert m.outputs == [7] and m.mem[8] == 0 and m.mem[9] == 0
    assert run("exercises", "five_to_one").outputs == [5, 4, 3, 2, 1]
    assert assemble("LOADI R1, 7")[:2] == [5, 7]
    assert len(assemble("HALT")) == 256
    for a in range(128):
        for b in range(0, 128, 7):
            assert run("exercises", "larger", [a, b]).outputs == [max(a, b)]
