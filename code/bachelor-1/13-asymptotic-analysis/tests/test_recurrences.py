"""Closed forms of recurrences, the master theorem's cases, and the solver."""

import sys
from functools import cache
from math import ceil, log2
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))
sys.path.insert(0, str(HERE.parent / "exercises"))

from exo_cost import doublings  # noqa: E402
from master import master  # noqa: E402
from solve_rec import identify  # noqa: E402


def test_cases():
    expected = {(1, 2, 0): "even", (2, 2, 1): "even", (3, 2, 1): "leaves",
                (8, 2, 2): "leaves", (7, 2, 2): "leaves", (2, 2, 2): "root",
                (4, 2, 2): "even", (9, 3, 2): "even", (2, 4, 1): "root",
                (1, 3, 1): "root", (5, 2, 2): "leaves"}
    for (a, b, k), case in expected.items():
        assert master(a, b, k)[0] == case
        assert identify(a, b, k)[0] == case


@cache
def floors(n):  # T(1) = 0, T(n) = T(floor(n/2)) + T(ceil(n/2)) + n
    return 0 if n == 1 else floors(n // 2) + floors((n + 1) // 2) + n


def test_floors():
    for n in range(1, 3000):
        c = ceil(log2(n)) if n > 1 else 0
        assert floors(n) == n * c + n - 2**c
        assert n * log2(n) <= floors(n) <= n * log2(n) + n


def test_exact_solutions():
    t, u = 0, 0  # T(n) = T(n-1) + n and U(n) = 2U(n-1) + 1, both 0 at 0
    for n in range(1, 60):
        t, u = t + n, 2 * u + 1
        assert t == n * (n + 1) // 2 and u == 2**n - 1


def test_doublings_linear():
    for n in [2**6, 2**10, 1000, 3000]:
        assert doublings(n) <= 2 * n
