"""Binary search against the standard library's bisect, on random sorted lists."""

import bisect
import sys
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))
sys.path.insert(0, str(HERE.parent / "exercises"))

from bsearch import leftmost  # noqa: E402
from bsearch_bug import search  # noqa: E402
from rightmost import rightmost  # noqa: E402

sorted_lists = st.lists(st.integers(-20, 20), max_size=40).map(sorted)


@given(sorted_lists, st.integers(-25, 25))
def test_leftmost_rightmost(a, x):
    assert leftmost(a, x) == bisect.bisect_left(a, x)
    assert rightmost(a, x) == bisect.bisect_right(a, x)
    i = leftmost(a, x)
    assert all(y < x for y in a[:i]) and all(y >= x for y in a[i:])  # the postcondition


def test_iterations_bound():
    for n in range(1, 300):
        a, worst = list(range(n)), 0
        for x in range(-1, n + 1):
            lo, hi, steps = 0, n, 0
            while lo < hi:
                mid = lo + (hi - lo) // 2
                lo, hi = (mid + 1, hi) if a[mid] < x else (lo, mid)
                steps += 1
            worst = max(worst, steps)
        assert worst == n.bit_length()  # floor(log2 n) + 1


def test_bug_gets_stuck():
    assert search([2, 5, 8], 5) == 1 and search([2, 5, 8], 9) == -1
    assert str(search([2, 5, 8], 1)).startswith("stuck")
