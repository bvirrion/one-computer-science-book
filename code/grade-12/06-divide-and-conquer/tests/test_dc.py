import importlib.util
import io
import math
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_merge_sort_and_counts():
    ms = load("listings", "merge_sort")
    rng = random.Random(4)
    for h in range(0, 9):
        n = 2 ** h
        for _ in range(20):
            t = [rng.randint(0, 50) for _ in range(n)]
            s, c = ms.merge_sort(t)
            assert s == sorted(t)
            assert n * h // 2 <= c <= n * h
    for n in range(0, 40):
        t = [rng.random() for _ in range(n)]
        assert ms.merge_sort(t)[0] == sorted(t)


def test_fast_power():
    fp = load("listings", "fast_power")
    for n in range(0, 300):
        value, m = fp.power(3, n)
        assert value == 3 ** n == fp.power_loop(3, n)
        if n >= 1:
            assert m <= 2 * int(math.log2(n))
            assert m == n.bit_length() - 1 + bin(n).count("1") - 1
        assert fp.power_mod(7, n, 1009) == pow(7, n, 1009)


def test_rotation(monkeypatch):
    rc = load("listings", "rotate_copy")
    rq = load("listings", "rotate_quadrants")
    ex = load("exercises", "dc_ex")
    rng = random.Random(7)
    for k in range(0, 5):
        n = 2 ** k
        g = [[rng.randint(0, 9) for _ in range(n)] for _ in range(n)]
        h = [row[:] for row in g]
        rq.rotate_in_place(h)
        assert h == rc.rotate_copy(g)
    for n in range(1, 9):
        g = [[rng.randint(0, 9) for _ in range(n)] for _ in range(n)]
        h = [row[:] for row in g]
        ex.rotate_layers(h)
        assert h == rc.rotate_copy(g)
    monkeypatch.chdir(HERE / "listings")
    load("listings", "rotate_image")


def test_inversions():
    inv = load("listings", "inversions")
    rng = random.Random(9)
    for n in range(0, 60):
        t = rng.sample(range(n), n)
        s, c = inv.sort_count(t)
        assert s == sorted(t) and c == inv.inversions_brute(t)
    t = inv.compare(inv.ranking(100_000, 1), inv.ranking(100_000, 2))
    assert inv.sort_count(t)[1] == 2488902981


def test_exercises():
    ex = load("exercises", "dc_ex")
    rng = random.Random(2)
    for _ in range(200):
        a = sorted((rng.randint(0, 20) for _ in range(rng.randint(0, 6))), reverse=True)
        b = sorted((rng.randint(0, 20) for _ in range(rng.randint(0, 6))), reverse=True)
        assert ex.merge_desc(a, b) == sorted(a + b, reverse=True)
        t = [rng.randint(-9, 9) for _ in range(rng.randint(1, 12))]
        best = max(sum(t[i:j]) for i in range(len(t)) for j in range(i + 1, len(t) + 1))
        assert ex.max_subarray(t) == best
        assert ex.merge_sort_bottom_up(t) == sorted(t)
    f = [0, 1]
    for _ in range(100):
        f.append(f[-1] + f[-2])
    assert all(ex.fib(n) == f[n] for n in range(100))
    assert ex.merge_no_tail([1, 4, 9], [2, 3]) == [1, 2, 3]
