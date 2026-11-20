"""Tests of chapter 10: every listing and exercise program run on rv with several inputs."""

from pathlib import Path

import pytest
from rv import RVFault, assemble, decode, encode, run_source

HERE = Path(__file__).resolve().parent.parent
LST = HERE / "listings"
EXO = HERE / "exercises"


def run(path, inputs=(), steps=1_000_000):
    return run_source(path.read_text(), inputs=list(inputs), max_steps=steps)


def check_digit(code):
    digits = [int(c) for c in reversed(str(code))]
    s = sum((3 if i % 2 == 0 else 1) * d for i, d in enumerate(digits))
    return (10 - s % 10) % 10


@pytest.mark.parametrize(
    "name, expected",
    [
        ("hook.S", "413"),
        ("first.S", "5050\n"),
        ("memory.S", "78 56 34 12 -1 255 32767 "),
        ("array_sum.S", str(65 + 133 + 412 + 98 + 251 + 320)),
        ("strlen.S", str(len("Quay Street"))),
        ("if_while.S", "42 111"),
        ("factorial.S", "6"),
        ("struct_access.S", str(65 + 412)),
        ("switch_table.S", "50 10 20 0 5 "),
        ("clobber_bug.S", "61"),
    ],
)
def test_listing_outputs(name, expected):
    out, status, _ = run(LST / name)
    assert (out, status) == (expected, 0)


def test_misaligned_faults():
    with pytest.raises(RVFault, match="misaligned word load"):
        run(LST / "misaligned.S")


@pytest.mark.parametrize("code", [7, 4006, 9780306, 978030640, 12, 123456789, 100000000])
def test_check_digit_and_count(code):
    out, status, stats = run(LST / "count.S", [code])
    assert out == f"{code}\n{check_digit(code)}\n" or out == f"{check_digit(code)}\n"
    n = len(str(code))
    assert stats["instructions"] == 14 * n + 26  # the problem's formula


def test_constants_li():
    for n in [0, 1, -1, 2047, 2048, -2048, -2049, 0x12345678, 0x12345FFF, 0x7FFFF000, 0x7FFFFFFF]:
        prog = assemble(f"main: li a0, {n}\n li a7, 1\n ecall\n li a0, 0\n ret\n")
        hi = ((n + 0x800) >> 12) & 0xFFFFF
        lo = n & 0xFFF
        lo = lo - 4096 if lo >= 2048 else lo
        assert ((hi << 12) + lo) & 0xFFFFFFFF == n & 0xFFFFFFFF  # the proposition
        out, _, _ = run_source(prog_text(n))
        assert int(out) == (n if n < 2**31 else n - 2**32)
        assert len(prog.words) in (5, 6)


def prog_text(n):
    return f"main: li a0, {n}\n li a7, 1\n ecall\n li a0, 0\n ret\n"


def test_exo_programs():
    assert run(EXO / "max.S")[0] == "19"
    assert run(EXO / "strcmp.S")[0] == "-1 0 -1 "
    assert run(EXO / "loan_fine.S")[0] == "90 0 2000 "
    for n, f in [(0, 0), (1, 1), (2, 1), (10, 55), (15, 610)]:
        out, _, stats = run(EXO / "fib.S", [n])
        assert out.split()[-1] == str(f)
    assert run(EXO / "switch2.S")[0] == "ABB?D??"
    assert run(EXO / "exo_ra_fixed.S")[0] == "42"


def test_fib_calls():
    # calls of fib(n): C(n) = 2 F(n+1) - 1; jumps count every jal/jalr
    fibs = [0, 1]
    for _ in range(20):
        fibs.append(fibs[-1] + fibs[-2])
    for n in range(0, 12):
        prog = (EXO / "fib.S").read_text()
        _, _, stats = run_source(prog, inputs=[n])
        calls = 2 * fibs[n + 1] - 1
        # each call of fib is one jal and one ret; main adds its own call to fib and its ret
        assert stats["jumps"] == 2 * calls + 1


@pytest.mark.parametrize("key, index", [(65, 0), (189, 3), (412, 6), (98, 1), (100, -1), (1, -1), (999, -1)])
def test_bsearch(key, index):
    out, status, _ = run(EXO / "bsearch.S", [key])
    assert out.split()[-1] == str(index)


def test_encodings_by_hand():
    assert encode("addi", rd=10, rs1=10, imm=-1) == 0xFFF50513
    assert encode("sw", rs1=2, rs2=1, imm=12) == 0x00112623
    assert decode(0x00B50633).mnemonic == "add"
    assert decode(0x00452283).imm == 4
    assert decode(0xFE0518E3).imm == -16
    assert decode(0x00C000EF).imm == 12
