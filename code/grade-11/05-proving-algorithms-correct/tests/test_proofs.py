import importlib.util
import io
import random
from contextlib import redirect_stdout
from pathlib import Path

import pytest

HERE = Path(__file__).parent.parent


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_sorts_and_largest():
    rng = random.Random(1)
    lg = load("listings", "largest")
    ss = load("listings", "selection_sort")
    ins = load("listings", "insertion_sort")
    for _ in range(300):
        t = [rng.randint(-20, 20) for _ in range(rng.randint(1, 12))]
        assert lg.largest(t) == max(t)
        for sort in (ss.selection_sort, ins.insertion_sort):
            u = list(t)
            with redirect_stdout(io.StringIO()):
                sort(u)
            assert u == sorted(t)


def test_search():
    bs = load("listings", "binary_search")
    rng = random.Random(2)
    for _ in range(300):
        t = sorted(rng.sample(range(100), rng.randint(0, 15)))
        for x in range(-1, 101):
            with redirect_stdout(io.StringIO()):
                i = bs.search(t, x)
            assert (i is None and x not in t) or t[i] == x
    bug = load("listings", "binary_search_bug")
    with pytest.raises(RuntimeError):
        bug.search([3, 8, 12], 10)


def test_isqrt():
    sq = load("listings", "isqrt")
    for n in range(3000):
        assert sq.isqrt_linear(n)[0] == sq.isqrt_halving(n)[0]


def test_exercises():
    ex = load("exercises", "proofs_ex")
    assert ex.largest_bug([4, 9, 2, 11]) == 9
    assert ex.index_of_min([5, 3, 8, 1, 9], 2) == 3
    t = [3, 8, 12, 15, 21, 30, 34, 41, 47, 52]
    assert [x for x in t if ex.search_bug(t, x) is None] == [8, 21, 41]
    assert ex.total([4, 7, 1]) == 12 and ex.count([1, 2, 1, 1], 1) == 3
    assert ex.is_sorted([1, 2, 2, 5]) and not ex.is_sorted([2, 1])
    assert ex.collatz_turns(27) == 111
    for lo in range(5):
        for hi in range(lo, 12):
            for k in range(lo, hi + 1):
                assert ex.first_true(lambda m, k=k: m >= k, lo, hi) == k
