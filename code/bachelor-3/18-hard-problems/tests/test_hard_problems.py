import itertools
import math
import random
import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

import ex5_learning  # noqa: E402
import ex6_one_tree  # noqa: E402
import ex12_restarts  # noqa: E402
import horn  # noqa: E402
import knapsack_bb  # noqa: E402
import set_cover  # noqa: E402
import tsp  # noqa: E402
import vertex_cover  # noqa: E402
import walksat  # noqa: E402
from cdcl import CDCL  # noqa: E402


def brute(clauses, n):
    return any(all(any(b[abs(x) - 1] == (x > 0) for x in c) for c in clauses)
               for b in itertools.product((False, True), repeat=n))


def satisfies(a, clauses):
    return all(any(a.get(abs(x), False) == (x > 0) for x in c) for c in clauses)


cnf = st.integers(1, 7).flatmap(lambda n: st.tuples(st.just(n), st.lists(
    st.lists(st.integers(1, n).flatmap(lambda v: st.sampled_from((v, -v))),
             min_size=1, max_size=3), min_size=1, max_size=30)))
graphs = st.integers(2, 9).flatmap(lambda n: st.tuples(st.just(n), st.lists(
    st.sampled_from(list(itertools.combinations(range(n), 2))), unique=True)))
points = st.lists(st.tuples(st.just("p"), st.integers(0, 1000), st.integers(0, 1000)),
                  min_size=4, max_size=8, unique_by=lambda p: p[1:])


@given(graphs)
def test_matching_cover_is_a_cover_within_twice_the_minimum(g):
    n, edges = g
    cover = vertex_cover.matching_cover(edges)
    assert all(u in cover or v in cover for u, v in edges)
    assert len(cover) <= 2 * len(vertex_cover.minimum_cover(n, edges))


def test_greedy_set_cover_within_harmonic_bound():
    rng = random.Random(1)
    for _ in range(100):
        n = 12
        sets = [set(rng.sample(range(n), rng.randrange(1, 6))) for _ in range(9)]
        sets.append(set(range(n // 2)))
        sets.append(set(range(n // 2, n)))
        g = set_cover.greedy(range(n), sets)
        assert set().union(*(sets[i] for i in g)) == set(range(n))
        harmonic = sum(1 / k for k in range(1, n + 1))
        assert len(g) <= harmonic * len(set_cover.exact(range(n), sets)) + 1e-9


@settings(max_examples=40, deadline=None)
@given(points)
def test_tours(pts):
    best = min(tsp.length(pts, [0, *p]) for p in itertools.permutations(range(1, len(pts))))
    hk = tsp.held_karp(pts)
    assert sorted(hk) == list(range(len(pts)))
    assert math.isclose(tsp.length(pts, hk), best)
    doubled = tsp.tree_doubling(pts)
    assert sorted(doubled) == list(range(len(pts)))
    assert tsp.length(pts, doubled) <= 2 * best + 1e-6
    improved = tsp.two_opt(pts, doubled)
    assert sorted(improved) == list(range(len(pts)))
    assert tsp.length(pts, improved) <= tsp.length(pts, doubled) + 1e-6
    assert ex6_one_tree.one_tree_bound(pts) <= best + 1e-6


def test_town_has_30_places_and_the_van_ratio():
    places = tsp.town_places()
    assert len(places) == 30
    van = places[:12]
    assert 16_634 < tsp.length(van, tsp.held_karp(van)) < 16_636


@given(st.lists(st.tuples(st.integers(1, 30), st.integers(1, 30)), max_size=10),
       st.integers(0, 100))
def test_knapsack_bound_agrees_with_dynamic_programming(items, capacity):
    best = [0] * (capacity + 1)
    for w, v in items:
        for c in range(capacity, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    assert knapsack_bb.branch_and_bound(items, capacity, True)[0] == best[capacity]
    assert knapsack_bb.branch_and_bound(items, capacity, False)[0] == best[capacity]


@settings(max_examples=300)
@given(cnf)
def test_cdcl_agrees_with_brute_force(f):
    n, clauses = f
    a, _ = CDCL(clauses, n).solve()
    assert (a is not None) == brute(clauses, n)
    if a is not None:
        assert satisfies(a, clauses)


def test_first_uip_of_the_figure():
    clauses = [[-2, 3], [-1, -3, 4], [-3, 5], [-4, -5]]
    s = CDCL(clauses, 5)
    for decision in (1, 2):
        s.limits.append(len(s.trail))
        s.assign(decision, None)
        conflict = s.propagate()
    assert sorted(conflict) == [-5, -4]
    learned, back = s.analyse(conflict)
    assert learned == [-3, -1] and back == 1


@settings(max_examples=300)
@given(cnf)
def test_horn_sat_agrees_with_brute_force(f):
    n, clauses = f
    clauses = [c for c in clauses if sum(x > 0 for x in c) <= 1]
    a = horn.horn_sat(clauses, n)
    assert (a is not None) == brute(clauses, n)
    if a is not None:
        assert satisfies(a, clauses)


def test_forward_chaining_grandparents():
    facts, _ = horn.parent_facts()
    derived, _ = horn.forward_chain(facts, horn.RULES)
    parents = {(a, b) for _, a, b in facts}
    expected = {("grandparent", a, c) for a, b in parents for b2, c in parents if b == b2}
    assert {f for f in derived if f[0] == "grandparent"} == expected


def test_walksat_finds_assignments():
    clauses = [[1, 2, -3], [-1, 3, 4], [2, -4, 5], [-2, -5, 1], [3, 4, 5]]
    a, _ = walksat.walksat(clauses, 5, random.Random(0))
    assert satisfies(a, clauses)


def test_exercise_5_buggy_is_unsound_and_fixed_is_right():
    clauses = [[-3, 1, -2], [3, 2, 1], [-1, 3, -2], [-1, -2, -3], [3, 2, -1],
               [1, 2, -3], [2, 3, -1], [-2, -3, 1], [1, 3, -2]]
    assert brute(clauses, 3)
    assert ex5_learning.Buggy(clauses, 3).solve()[0] is None
    assert satisfies(ex5_learning.Fixed(clauses, 3).solve()[0], clauses)


@settings(max_examples=100)
@given(cnf)
def test_exercise_12_restarts_keep_the_answer(f):
    n, clauses = f
    a, _ = ex12_restarts.Restarting(clauses, n, unit=1).solve()
    assert (a is not None) == brute(clauses, n)


def test_exercise_12_sequence():
    assert [ex12_restarts.reluctant(i) for i in range(1, 16)] == [
        1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8]


def test_van_bounds_and_table_size():
    van = tsp.town_places()[:12]
    children = tsp.minimum_spanning_tree(van)
    mst = sum(tsp.dist(van[u], van[v]) for u in children for v in children[u])
    assert 11_366 < mst < 11_368
    assert 13_593 < ex6_one_tree.one_tree_bound(van) < 13_595
    states = sum(1 for s in range(2, 1 << 12, 2) for j in range(1, 12) if s >> j & 1)
    assert states == 11 * 2 ** 10


def test_exercise_12_counts():
    from sat_compare import random_3sat
    rng, counts = random.Random(18), []
    for n in (60, 80, 100):
        clauses, _ = random_3sat(n, 4.26, rng)
        a = CDCL(clauses, n).solve()[1]
        b = ex12_restarts.Restarting(clauses, n).solve()[1]
        counts.append((a["conflicts"], b["conflicts"], b["restarts"]))
    assert counts == [(119, 90, 4), (289, 212, 8), (101, 169, 6)]
