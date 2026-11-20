"""Merge, reverse, Ackermann, McCarthy's 91 function and the sorting game."""

import sys
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))
sys.path.insert(0, str(HERE.parent / "exercises"))

from ackermann import ack  # noqa: E402
from even_odd import is_even, is_odd  # noqa: E402
from merge import merge  # noqa: E402
from reverse_twice import rev  # noqa: E402
from sort_game import inversions, play  # noqa: E402

ints = st.lists(st.integers(-5, 5), max_size=20)


@given(ints, ints)
def test_merge(xs, ys):
    assert merge(sorted(xs), sorted(ys)) == sorted(xs + ys)


@given(ints, ints)
def test_rev(xs, ys):
    assert rev(rev(xs)) == xs
    assert rev(xs + ys) == rev(ys) + rev(xs)


def test_ackermann_closed_forms():
    for n in range(5):
        assert ack(1, n) == n + 2 and ack(2, n) == 2 * n + 3 and ack(3, n) == 2 ** (n + 3) - 3


def test_even_odd():
    assert all(is_even(n) == (n % 2 == 0) and is_odd(n) == (n % 2 == 1) for n in range(50))


def mccarthy(n):
    return n - 10 if n > 100 else mccarthy(mccarthy(n + 11))


def test_mccarthy_91():
    assert all(mccarthy(n) == 91 for n in range(-50, 102))
    assert all(mccarthy(n) == n - 10 for n in range(101, 200))


@given(ints)
def test_sort_game(xs):
    for choose in (min, max):
        result, moves = play(xs, choose)
        assert result == sorted(xs) and moves == inversions(xs)
