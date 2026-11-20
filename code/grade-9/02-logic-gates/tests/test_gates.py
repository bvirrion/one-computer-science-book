"""Grade 9, chapter 2: logic gates, every table checked on every input."""

import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "listings"))

from gates import AND, NOT, OR, XOR  # noqa: E402

BITS = [0, 1]


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()) as out:
        spec.loader.exec_module(module)
    return module, out.getvalue().splitlines()


def test_gates_and_laws():
    for a in BITS:
        assert NOT(NOT(a)) == a and AND(a, 1) == a and OR(a, 1) == 1 and OR(a, 0) == a
        for b in BITS:
            assert AND(a, b) == int(a and b) and OR(a, b) == int(a or b)
            assert XOR(a, b) == int(a != b)
            assert NOT(AND(a, b)) == OR(NOT(a), NOT(b))
            assert NOT(OR(a, b)) == AND(NOT(a), NOT(b))
            assert OR(a, AND(a, b)) == a


def test_circuits():
    half, _ = load("listings", "half_adder")
    nand, _ = load("listings", "nand_only")
    judges, lines = load("listings", "judges")
    for a in BITS:
        for b in BITS:
            s, c = half.half_adder(a, b)
            assert 2 * c + s == a + b
            assert nand.AND(a, b) == AND(a, b) and nand.OR(a, b) == OR(a, b)
            for c3 in BITS:
                want = int(a + b + c3 >= 2)
                assert judges.pairs(a, b, c3) == judges.majority(a, b, c3) == want
    assert lines[-2:] == ["all three agree on the 8 inputs: True", "rows for five judges: 32"]


def test_exercises():
    one, _ = load("exercises", "exactly_one")
    assert [one.exactly_one(a, b, c) for a in BITS for b in BITS for c in BITS] == [
        0, 1, 1, 0, 1, 0, 0, 0]
    _, bug = load("exercises", "table_bug")
    assert bug == ["0 0 0"]
    _, rows = load("exercises", "table_or_not")
    assert [r[-1] for r in rows] == ["0", "0", "1", "0", "1", "0", "1", "0"]
    agree, _ = load("exercises", "agree")
    assert agree.agree(lambda a, b: NOT(AND(a, b)), lambda a, b: OR(NOT(a), NOT(b)))
    assert not agree.agree(AND, OR)
    adder, _ = load("exercises", "two_bit_adder")
    for x in range(4):
        for y in range(4):
            c, s1, s0 = adder.add_two_bits(x // 2, x % 2, y // 2, y % 2)
            assert 4 * c + 2 * s1 + s0 == x + y
    assert NOT(OR(1, 0)) == 0
    # all 16 two-input tables are reachable from NAND (closure under composition)
    nand = lambda a, b: 1 - a * b  # noqa: E731
    tables = {(0, 0, 1, 1), (0, 1, 0, 1)}
    grown = True
    while grown:
        new = {tuple(nand(x[i], y[i]) for i in range(4)) for x in tables for y in tables}
        grown = not new <= tables
        tables |= new
    assert len(tables) == 16
