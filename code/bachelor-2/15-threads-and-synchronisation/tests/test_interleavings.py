"""The explorer on every model of the chapter and its exercises."""
from math import comb

import bakery_model
import cond_model
import office_model
import pytest
import sem_outcomes
from interleavings import (Model, counter, explore, flag_lock_thread, peterson,
                           peterson_thread, straight)


@pytest.mark.parametrize("m, n", [(0, 3), (1, 1), (2, 3), (4, 4), (8, 8), (5, 9)])
def test_interleavings_count(m, n):
    assert explore(straight(m, n))[0] == comb(m + n, m)


def test_three_threads_multinomial():
    model = Model({}, {t: [(f"{t}{k}", None, None) for k in range(3)] for t in "ABC"})
    assert explore(model)[0] == 1680                     # 9! / (3! 3! 3!)


def test_counter():
    total, bad, _, _, outs = explore(counter(1))
    assert (total, bad, dict(outs)) == (6, 4, {1: 4, 2: 2})
    total, bad, _, _, outs = explore(counter(2))         # exercise 1
    assert total == comb(8, 4) and set(outs) == {2, 3, 4}


def test_locks():
    flag = Model({"flag": 0}, {"A": flag_lock_thread(), "B": flag_lock_thread()})
    assert explore(flag)[1] > 0
    assert explore(peterson())[1:3] == (0, 0)
    swapped = [[t[1], t[0]] + t[2:] for t in (peterson_thread(0), peterson_thread(1))]
    model = Model({"flag0": 0, "flag1": 0, "turn": 0}, {"A": swapped[0], "B": swapped[1]})
    assert explore(model)[:2] == (60, 12)                # exercise 8


def test_office():
    o = office_model
    assert explore(o.office(o.naive, 1, 1))[:2] == (20, 12)
    assert explore(o.office(o.locked, 6, 4))[:3] == (70, 0, 0)
    assert explore(o.office(o.atomic, 6, 4))[:3] == (12870, 0, 0)
    assert explore(o.office(o.naive, 6, 4))[1] > 0


def test_exercise_models():
    assert explore(cond_model.model(False))[1] > 0
    assert explore(cond_model.model(True))[1:3] == (0, 0)
    assert explore(bakery_model.bakery())[1:3] == (0, 0)
    assert explore(bakery_model.no_choosing())[1] > 0
    outs = explore(sem_outcomes.model())[4]
    assert set(outs) == {"ABCDE", "ABDCE", "ACBDE", "BACDE", "BADCE"}
