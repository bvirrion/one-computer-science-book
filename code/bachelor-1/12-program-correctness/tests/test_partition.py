"""Partition, the three-colour flag, the minimal swaps, maximum and division."""

import sys
from collections import deque
from itertools import product
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))
sys.path.insert(0, str(HERE.parent / "exercises"))

from division import divide  # noqa: E402
from flag import flag  # noqa: E402
from maximum import maximum  # noqa: E402
from min_swaps import min_swaps  # noqa: E402
from partition import partition  # noqa: E402


@given(st.lists(st.integers(-9, 9), min_size=1, max_size=30))
def test_partition(a):
    b = list(a)
    k = partition(b, 0, len(b))
    assert sorted(b) == sorted(a)
    assert all(x < b[k] for x in b[:k]) and all(x >= b[k] for x in b[k + 1:])
    assert maximum(a) == max(a)


@given(st.lists(st.integers(0, 2), max_size=40))
def test_flag(a):
    b = list(a)
    swaps = flag(b)
    assert b == sorted(a)
    assert swaps >= min_swaps(a)


def bfs_swaps(a):
    target, start = tuple(sorted(a)), tuple(a)
    seen, queue = {start: 0}, deque([start])
    while queue:
        s = queue.popleft()
        if s == target:
            return seen[s]
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                t = list(s)
                t[i], t[j] = t[j], t[i]
                t = tuple(t)
                if t not in seen:
                    seen[t] = seen[s] + 1
                    queue.append(t)


def test_min_swaps_against_search():
    for n in range(7):
        for a in product(range(3), repeat=n):
            assert min_swaps(list(a)) == bfs_swaps(a)


@given(st.integers(0, 10**6), st.integers(1, 1000))
def test_divide(a, b):
    assert divide(a, b) == divmod(a, b)
