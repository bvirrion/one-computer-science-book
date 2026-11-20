import importlib.util
import io
import random
import sys
from contextlib import redirect_stdout
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def best_count(requests):
    """The largest set of pairwise compatible requests, by trying every subset."""
    for r in range(len(requests), 0, -1):
        for subset in combinations(requests, r):
            if all(a[2] <= b[1] or b[2] <= a[1] for a, b in combinations(subset, 2)):
                return r
    return 0


def test_change():
    cg = load("listings", "change_greedy")
    ce = load("listings", "change_exhaustive")
    ex = load("exercises", "greedy_ex")
    for a in range(0, 120):
        assert sum(cg.greedy_change(a, [1, 2, 5, 10, 20, 50])) == a
        assert len(cg.greedy_change(a, [1, 2, 5, 10, 20, 50])) == \
            ce.fewest(a, [1, 2, 5, 10, 20, 50])[0]
        assert ex.greedy_change(a, [1, 3, 4]) == cg.greedy_change(a, [1, 3, 4])
    assert ce.fewest(6, [1, 3, 4])[0] == 2 and len(cg.greedy_change(6, [1, 3, 4])) == 3
    assert ex.is_canonical_upto([1, 2, 5], 50) and not ex.is_canonical_upto([1, 3, 4], 10)


def test_activities():
    act = load("listings", "activities")
    ex = load("exercises", "greedy_ex")
    rng = random.Random(4)
    for _ in range(200):
        reqs = []
        for k in range(rng.randint(1, 8)):
            s = rng.randint(0, 12)
            reqs.append((str(k), s, s + rng.randint(1, 4)))
        assert len(act.earliest_end_first(reqs)) == best_count(reqs)
        assert len(ex.max_activities(reqs)) == best_count(reqs)
        assert len(ex.shortest_first(reqs)) <= best_count(reqs)
        hours = range(0, 17)
        assert ex.rooms_needed(reqs) == max(
            sum(1 for _, s, e in reqs if s <= h < e) for h in hours)


def test_knapsacks():
    kf = load("listings", "knapsack_fractional")
    ex = load("exercises", "greedy_ex")
    assert kf.fill(kf.GOODS, 15)[1] == 194
    assert kf.fill(kf.GOODS, 8)[1] == 134
    assert kf.fill(kf.GOODS, 10)[1] == 158 and ex.greedy_by_value(kf.GOODS, 10) == 132


def test_brenmoor():
    b = load("listings", "brenmoor")
    bad = b.failures(b.BRENMOOR, 100)
    assert bad[0] == 36 and len(bad) == 17
    assert not b.failures([1, 2, 5, 10, 25, 40], 200)
