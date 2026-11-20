"""Hand-computed cycle counts, and the invariants of the timing model."""
from pathlib import Path

import pytest
from btfn import BackwardTaken
from forwarding import fields, forward
from pipeline import schedule, steps_of
from predictor import OneBit, TwoBit

HERE = Path(__file__).resolve().parent.parent
LST = HERE / "listings"
PROGRAMS = ["loop_sum.S", "bubble_sort.S", "collatz.S", "load_use.S", "independent.S",
            "forwarding.S", "four.S"]


def steps(name, where=LST):
    return steps_of((where / name).read_text())


def test_hand_counts():
    assert schedule(steps("independent.S")).cycles == 5 + 4          # n + k - 1
    assert schedule(steps("load_use.S")).cycles == 9 + 4 + 2  # two load-use stalls
    assert schedule(steps("load_use.S"), forwarding=False).cycles == 23
    assert schedule(steps("forwarding.S")).cycles == 7 + 4  # everything forwarded
    # a two-turn loop: the taken branch costs 2 cycles under "not taken"
    loop = "main: li t0, 2\nl: addi t0, t0, -1\n bnez t0, l\n ret\n"
    assert schedule(steps_of(loop)).cycles == 6 + 4 + 2


@pytest.mark.parametrize("name", PROGRAMS)
@pytest.mark.parametrize("fwd", [False, True])
@pytest.mark.parametrize("pred", [None, OneBit, TwoBit])
def test_cycles_add_up(name, fwd, pred):
    s = steps(name)
    t = schedule(s, fwd, pred() if pred else None)
    assert t.cycles == len(s) + 4 + t.stalls + t.flushed
    for f, d, x in zip(t.fetch, t.decode, t.execute):
        assert f < d < x
    assert all(a < b for a, b in zip(t.execute, t.execute[1:]))  # in order, one per cycle


def test_ideal_speedup():
    for n in (1, 2, 5, 100):
        text = "main:\n" + " addi t0, zero, 1\n" * (n - 1) + " ret\n"
        cycles = schedule(steps_of(text)).cycles
        assert cycles == n + 4
        assert n * 5 / cycles == pytest.approx(n * 5 / (5 + n - 1))


def test_load_use_one_stall():
    for user in ["add t1, t0, t0", "sw t0, 4(a0)", "beq t0, zero, e", "addi t1, t0, 1"]:
        text = f"main: la a0, v\n lw t0, 0(a0)\n {user}\ne: ret\n .data\nv: .word 0, 0\n"
        assert schedule(steps_of(text)).stalls == 1
        text2 = f"main: la a0, v\n lw t0, 0(a0)\n nop\n {user}\ne: ret\n .data\nv: .word 0, 0\n"
        assert schedule(steps_of(text2)).stalls == 0


def test_reordered_loop():
    plain, sched = steps("loop_sum.S"), steps("loop_sum_sched.S", HERE / "exercises")
    assert len(plain) == len(sched)
    assert schedule(plain).stalls == 32 and schedule(sched).stalls == 0
    assert schedule(sched).cycles == schedule(plain).cycles - 32


def test_backward_taken():
    s = steps("loop_sum.S")
    assert schedule(s, True, BackwardTaken(s)).mispredicted == 1


def test_forwarding_unit():
    # every operand read in EX must come from the newest earlier writer of that register
    for name in ["forwarding.S", "collatz.S", "four.S"]:
        s = steps(name)
        for k in range(len(s)):
            ahead = [fields(s[k - j])[:2] if k >= j else (False, 0) for j in (1, 2)]
            _, _, rs1, _ = fields(s[k])
            newest = next((j for j in (1, 2) if k >= j and fields(s[k - j])[0]
                           and fields(s[k - j])[1] == rs1 and rs1 != 0), None)
            want = {1: "EX/MEM", 2: "MEM/WB", None: "register file"}[newest]
            assert forward(rs1, *ahead) == want
    assert forward(0, (True, 0), (False, 0)) == "register file"
    assert forward(0, (True, 0), (False, 0), check_x0=False) == "EX/MEM"
