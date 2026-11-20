import importlib.util
import io
import math
import random
import sys
from contextlib import redirect_stdout
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_fibonacci():
    memo = load("listings", "fib_memo")
    table = load("listings", "fib_table")
    f = table.fib_table(200)
    for n in range(0, 25):
        memo.calls = 0
        assert memo.fib_naive(n) == f[n]
        memo.calls = 0
        assert memo.fib_memo(n) == f[n] == table.fib_two(n)
        assert memo.calls == max(1, 2 * n - 1)


def fewest_by_trying(amount, coins):
    for count in range(amount + 1):
        for combo in product(coins, repeat=count):
            if sum(combo) == amount:
                return count
    return None


def test_change():
    ch = load("listings", "change_dp")
    ex = load("exercises", "dp_ex")
    for coins in [[1, 3, 4], [1, 5, 10, 25], [2, 5], [1, 2, 5, 12, 25, 40]]:
        best, last = ch.change_table(13, coins)
        for a in range(14):
            assert best[a] == fewest_by_trying(a, coins) == ex.min_coins(a, coins)
            if best[a] is not None:
                used = ch.rebuild(a, last)
                assert sum(used) == a and len(used) == best[a]


def lcs_by_trying(a, b):
    for r in range(len(a), -1, -1):
        for keep in combinations(range(len(a)), r):
            s = [a[i] for i in keep]
            it = iter(b)
            if all(x in it for x in s):
                return r


def test_lcs_and_alignment():
    lcs = load("listings", "lcs")
    al = load("listings", "align")
    vs = load("listings", "versions")
    ex = load("exercises", "dp_ex")
    rng = random.Random(3)
    for _ in range(150):
        a = "".join(rng.choice("ABC") for _ in range(rng.randint(0, 7)))
        b = "".join(rng.choice("ABC") for _ in range(rng.randint(0, 7)))
        t = lcs.lcs_table(a, b)
        assert t[len(a)][len(b)] == lcs_by_trying(a, b) == len(lcs.rebuild(a, b, t))
        d = al.distance_table(a, b)
        pairs = al.alignment(a, b, d)
        assert "".join(x for x, _ in pairs if x) == a
        assert "".join(y for _, y in pairs if y) == b
        assert sum(x != y for x, y in pairs) == d[len(a)][len(b)]
        assert vs.distance_two_rows(a, b) == d[len(a)][len(b)]
        assert len(ex.edit_operations(a, b)) == d[len(a)][len(b)]
    w, o = vs.OLD.split(), vs.NEW.split()
    assert al.distance_table(w, o)[len(w)][len(o)] == 15


def test_knapsack():
    kn = load("listings", "knapsack_dp")
    rng = random.Random(5)
    for _ in range(60):
        objs = [(str(i), rng.randint(1, 8), rng.randint(1, 50))
                for i in range(rng.randint(0, 7))]
        cap = rng.randint(0, 20)
        k = kn.knapsack(objs, cap)
        assert k[len(objs)][cap] == kn.every_subset(objs, cap)
        names = kn.chosen(objs, k, cap)
        picked = [o for o in objs if o[0] in names]
        assert sum(o[1] for o in picked) <= cap
        assert sum(o[2] for o in picked) == k[len(objs)][cap]


def test_exercises():
    ex = load("exercises", "dp_ex")
    for n in range(12):
        for k in range(n + 1):
            assert ex.binomial(n, k) == math.comb(n, k)
    assert ex.binomial_bad(10, 5) != 252
    assert ex.lcs_wrong_order("LIBRARY", "LITERARY") != 6
    assert ex.grid_paths(5, 5) == 252 == math.comb(10, 5)
    rng0 = random.Random(1)
    for _ in range(100):
        old = [rng0.choice("abcd") for _ in range(rng0.randint(0, 6))]
        new = [rng0.choice("abcd") for _ in range(rng0.randint(0, 6))]
        out = ex.diff_lines(old, new)
        assert [x[2:] for x in out if x[0] != "+"] == old
        assert [x[2:] for x in out if x[0] != "-"] == new
    rng = random.Random(8)
    for _ in range(100):
        t = [rng.randint(0, 9) for _ in range(rng.randint(0, 9))]
        s = ex.longest_increasing(t)
        assert all(x < y for x, y in zip(s, s[1:]))
        assert len(s) == max((r for r in range(len(t) + 1)
                              for c in combinations(t, r)
                              if all(x < y for x, y in zip(c, c[1:]))), default=0)
