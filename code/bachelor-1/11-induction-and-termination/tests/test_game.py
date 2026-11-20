"""The game that always ends: every play has the length given by the potential."""

import sys
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "listings"))

from game import lengths, moves, plays, potential  # noqa: E402


def test_every_play_has_the_potential_length():
    for n in range(1, 4):
        for start in product(range(4), repeat=n):
            assert lengths(start) == {potential(start)}


def test_each_move_lowers_the_potential_by_one():
    for start in product(range(5), repeat=3):
        assert all(potential(s) == potential(start) - 1 for s in moves(start))


def test_single_counts():
    assert [potential((k,)) for k in range(6)] == [0, 1, 3, 7, 15, 31]
    assert plays((2,)) == 2 and plays((1, 1)) == 2
