"""The printed listings and exercise solutions of grade 6, chapter 3."""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def out(folder, name):
    r = subprocess.run([sys.executable, name], cwd=HERE / folder, capture_output=True, text=True)
    assert r.returncode == 0
    return r.stdout.splitlines()


def test_count_and_ranges():
    assert out("listings", "count.py") == [f"i is {i}" for i in range(5)] + ["done"]
    assert out("listings", "ranges.py") == "3 4 5 6 --- 0 5 10 15 --- 10 7 4 1".split()


def test_nested_and_stairs():
    rows = out("listings", "times_table.py")
    assert [list(map(int, r.split())) for r in rows] == [[r * c for c in range(1, 6)] for r in range(1, 6)]
    assert out("listings", "stairs.py") == ["#" * n for n in range(1, 6)]
    assert out("listings", "not_indented.py") == ["Hip,"] * 3 + ["hooray!"]


def test_exercise_solutions():
    assert out("exercises", "hip.py") == ["Hip,", "hooray!"] * 3
    assert out("exercises", "seven.py") == [f"7 x {i} = {7 * i}" for i in range(1, 11)]
    assert len(out("exercises", "nested_count.py")) == 12
    terms = list(map(int, out("exercises", "sequence.py")[0].split()))
    assert terms[:4] == [1, 4, 7, 10] and len(terms) == 20 and terms[-1] == 58
    assert list(range(2, 10, 3)) == [2, 5, 8]
