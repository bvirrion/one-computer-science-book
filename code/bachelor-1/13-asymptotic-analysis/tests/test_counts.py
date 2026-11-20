"""Counts of insertion sort, merge sort, the three duplicate finders, and loops."""

import random
import sys
from fractions import Fraction
from itertools import permutations
from math import factorial
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))
sys.path.insert(0, str(HERE.parent / "exercises"))

from count_ops import insertion_sort  # noqa: E402
from duplicates import BOOKS, by_pairs, by_set, by_sorting  # noqa: E402
from nested_count import closed_form, count_triples  # noqa: E402
from sorts import maximum, merge_sort  # noqa: E402


@given(st.lists(st.integers(-50, 50), max_size=60))
def test_sorts(a):
    b = list(a)
    insertion_sort(b)
    assert b == sorted(a) == merge_sort(a, [0])


def test_best_worst_average():
    for n in range(1, 40):
        assert insertion_sort(list(range(n))) == n - 1
        assert insertion_sort(list(range(n, 0, -1))) == n * (n - 1) // 2
    for n in range(1, 7):
        total = sum(insertion_sort(list(p)) for p in permutations(range(n)))
        h = sum(Fraction(1, k) for k in range(1, n + 1))
        assert Fraction(total, factorial(n)) == Fraction(n * (n - 1), 4) + n - h


def test_merge_sort_bound():
    rng = random.Random(1)
    for n in [2, 3, 7, 64, 100, 1000]:
        c = [0]
        merge_sort(rng.sample(range(n), n), c)
        assert c[0] <= n * (n - 1).bit_length()  # at most n ceil(log2 n)
        m = [0]
        maximum(list(range(n)), m)
        assert m[0] == n - 1


def test_duplicates():
    for n in [10, 25, 77, 400]:
        xs = BOOKS[:n]
        truth = {x for x in xs if xs.count(x) > 1}
        (f1, o1), (f2, _), (f3, o3) = by_pairs(xs), by_sorting(xs), by_set(xs)
        assert f1 == f2 == f3 == truth
        assert o1 == n * (n - 1) // 2 and o3 == n


def test_nested():
    for n in range(12):
        assert count_triples(n) == closed_form(n)
