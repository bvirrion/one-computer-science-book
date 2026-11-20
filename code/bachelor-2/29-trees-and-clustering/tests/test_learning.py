import math
import random
from collections import Counter

from hypothesis import given, settings
from hypothesis import strategies as st

from dataset import loans, rule
from hac import cut, hac, kruskal_forest
from id3 import accuracy, best_split, depth, entropy, id3
from kdtree import build, dist2, nearest
from kmeans import assign, centroid, cost, lloyd
from knn import evaluate


@settings(max_examples=100, deadline=None)
@given(st.integers(0, 10**6))
def test_kd_nearest_equals_brute_force(seed):
    rng = random.Random(seed)
    pts = [(rng.randrange(20), rng.randrange(20)) for _ in range(rng.randrange(1, 40))]
    tree = build(pts)
    for _ in range(10):
        q = (rng.uniform(-5, 25), rng.uniform(-5, 25))
        _, d = nearest(tree, q)
        assert d == min(dist2(p, q) for p in pts)


@settings(max_examples=60, deadline=None)
@given(st.integers(0, 10**6))
def test_lloyd_cost_never_increases(seed):
    rng = random.Random(seed)
    pts = [(rng.random(), rng.random()) for _ in range(rng.randrange(5, 60))]
    k = rng.randrange(1, 5)
    centres = rng.sample(pts, k)
    _, a, costs = lloyd(pts, centres)
    assert all(b <= c + 1e-9 for c, b in zip(costs, costs[1:]))
    # each step separately: the centroid step, then the assignment step
    a0 = assign(pts, centres)
    c1 = [centroid([p for p, j in zip(pts, a0) if j == i]) or centres[i] for i in range(k)]
    assert cost(pts, c1, a0) <= cost(pts, centres, a0) + 1e-9
    assert cost(pts, c1, assign(pts, c1)) <= cost(pts, c1, a0) + 1e-9


@settings(max_examples=60, deadline=None)
@given(st.integers(0, 10**6))
def test_single_linkage_is_the_spanning_tree_cut(seed):
    rng = random.Random(seed)
    pts = [(rng.random(), rng.random()) for _ in range(rng.randrange(2, 14))]
    merges = hac(pts, min)
    for k in range(1, len(pts) + 1):
        assert cut(merges, len(pts), k) == kruskal_forest(pts, k)


def test_id3_recovers_the_planted_rule():
    tree = id3(loans(700, seed=1))
    assert depth(tree) == 2
    test = loans(2000, seed=9)
    assert accuracy(tree, test) == 1.0
    assert all(y == rule(x) for x, y in test)


@settings(max_examples=200, deadline=None)
@given(st.lists(st.tuples(st.integers(0, 5), st.integers(0, 1)), min_size=2, max_size=30))
def test_information_gain_is_never_negative(pairs):
    data = [({"days": v, "pages": 0, "age": 0, "prior": 0, "distance": 0}, y)
            for v, y in pairs]
    h = entropy(Counter(y for _, y in data))
    n = len(data)
    for t in {v for v, _ in pairs}:
        left = Counter(y for (x, y) in data if x["days"] <= t)
        right = Counter(y for (x, y) in data if x["days"] > t)
        rest = sum(sum(c.values()) / n * entropy(c) for c in (left, right) if c)
        assert h - rest >= -1e-12
    split = best_split(data)
    assert split is None or split[0] > 0


def test_entropy_values():
    assert entropy(Counter({0: 5, 1: 5})) == 1.0
    assert entropy(Counter({0: 7})) == 0.0
    assert abs(entropy(Counter({0: 1, 1: 1, 2: 1, 3: 1})) - 2.0) < 1e-12
    assert math.isclose(entropy(Counter({0: 3, 1: 1})), 0.8112781244591328)


def test_knn_scaling_matters():
    train, test = loans(300, seed=1, noise=0.1), loans(100, seed=2, noise=0.1)
    assert evaluate(train, test, 5) > evaluate(train, test, 5, scale=False)
