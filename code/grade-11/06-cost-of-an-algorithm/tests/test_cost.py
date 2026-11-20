import importlib.util
import io
import random
import sys
import time
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


def test_counts():
    ci = load("listings", "count_insertion")
    cl = load("listings", "count_linear")
    for n in range(1, 60):
        assert ci.insertion_sort(list(range(n))) == n - 1
        assert ci.insertion_sort(list(range(n, 0, -1))) == n * (n - 1) // 2
        assert cl.search(list(range(n)), -1) == (None, n)
    t = random.Random(3).sample(range(50), 50)
    ci.insertion_sort(t)
    assert t == list(range(50))


def test_halvings_and_binary():
    hv = load("listings", "halvings")
    ex = load("exercises", "cost_ex")
    for n in range(1, 5000):
        k = hv.h(n)
        assert 2**k <= n < 2**(k + 1) and ex.h(n) == k
    for n in range(1, 300):
        worst = max(ex.binary_comparisons(n, x) for x in range(-1, n + 1))
        assert worst <= hv.h(n) + 1
        assert worst == hv.h(n) + 1


def test_exercises():
    ex = load("exercises", "cost_ex")
    for n in range(30):
        assert ex.double_loop(n) == ex.selection_count(n) == n * (n - 1) // 2
    assert ex.has_duplicate([3, 1, 3]) and not ex.has_duplicate([1, 2, 3])
    assert ex.duplicates_by_sorting([5, 2, 5]) == (True, 2)
    assert ex.count_comparisons(sorted, list(range(10))) == 9
    table = ex.growth_table()
    assert table["n * n"][2] > table["100 n"][2] > table["n * h(n)"][2]


def test_duplicates_shape():
    d = load("listings", "duplicates")
    rng = random.Random(5)
    values = rng.sample(range(100000), 3000)
    for find in (d.by_pairs, d.by_sorting, d.by_set):
        assert not find(values) and find(values + [values[17]])
    start = time.perf_counter()
    d.by_pairs(values)
    slow = time.perf_counter() - start
    start = time.perf_counter()
    d.by_sorting(values)
    assert time.perf_counter() - start < slow   # the shape of the measured result
