"""The two-bit proposition on synthetic loop traces, and the counts printed by branches.py."""
from pathlib import Path

from pipeline import steps_of
from predictor import NotTaken, OneBit, TwoBit, mispredictions

HERE = Path(__file__).resolve().parent.parent


def nested(outer, m):
    """The inner loop's closing branch: taken m - 1 times, then not taken, outer times."""
    return [(0x100, i < m - 1) for _ in range(outer) for i in range(m)]


def test_two_bit_proposition():
    for m in (2, 3, 10, 50):
        for outer in (1, 5, 20):
            trace = nested(outer, m)
            # the first execution warms the counter up; after that, one miss per execution
            assert mispredictions(trace, TwoBit(start=3)) == outer
            assert mispredictions(trace, OneBit()) == 2 * outer  # entry and exit, every time


def test_printed_counts():
    want = {"loop_sum.S": (32, 31, [31, 2, 2]), "bubble_sort.S": (272, 176, [176, 86, 60]),
            "collatz.S": (942, 186, [186, 315, 161])}
    for name, (n, taken, wrong) in want.items():
        steps = steps_of((HERE / "listings" / name).read_text())
        trace = [(s.pc, s.branch_taken) for s in steps if s.kind == "branch"]
        assert (len(trace), sum(t for _, t in trace)) == (n, taken)
        assert [mispredictions(trace, p()) for p in (NotTaken, OneBit, TwoBit)] == wrong
