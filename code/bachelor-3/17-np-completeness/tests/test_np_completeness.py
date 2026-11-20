"""Tests for chapter 17: every reduction checked against brute force on random small
instances, the Cook-Levin formula's counts, 2-SAT, the DP, and the exercises."""
import itertools
import os
import random
import sys

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = os.path.dirname(os.path.abspath(__file__))
for d in ("listings", "exercises"):
    sys.path.insert(0, os.path.join(HERE, "..", d))

import cook_levin  # noqa: E402
import ex5_clique  # noqa: E402
import ex6_col_to_sat  # noqa: E402
import reduce_3sat  # noqa: E402
import reduce_col  # noqa: E402
import reduce_is  # noqa: E402
import reduce_ss  # noqa: E402
import subset_dp  # noqa: E402
import two_sat  # noqa: E402
from cnf import (brute_force, has_independent_set, is_colourable,  # noqa: E402
                 random_3cnf, satisfies, subset_sums_to)
from dpll import dpll  # noqa: E402

EVERY = [[a * 1, b * 2, c * 3] for a in (1, -1) for b in (1, -1) for c in (1, -1)]


def literal(n):
    return st.integers(1, n).flatmap(lambda v: st.sampled_from((v, -v)))


cnf = st.lists(st.lists(literal(4), min_size=1, max_size=6), min_size=1, max_size=6)
three_cnf = st.lists(st.lists(st.integers(1, 4), min_size=3, max_size=3, unique=True)
                     .flatmap(lambda vs: st.tuples(*(st.sampled_from((v, -v))
                                                     for v in vs))).map(list),
                     min_size=1, max_size=7)


@settings(max_examples=300, deadline=None)
@given(cnf)
def test_to_3sat(f):
    g = reduce_3sat.to_3sat(f)
    assert all(len(c) == 3 for c in g)
    assert (brute_force(f) is None) == (brute_force(g) is None)


@settings(max_examples=200, deadline=None)
@given(three_cnf)
def test_independent_set_clique_cover(f):
    vertices, edges, k = reduce_is.to_independent_set(f)
    n = len(vertices)
    sat = brute_force(f) is not None
    assert has_independent_set(n, edges, k) == sat
    _, comp, kc = reduce_is.to_clique(n, edges, k)
    assert has_independent_set(n, [e for e in itertools.combinations(range(n), 2)
                                   if e not in set(comp)], kc) == sat


@settings(max_examples=100, deadline=None)
@given(three_cnf)
def test_colouring_counts_and_equivalence(f):
    size, edges = reduce_col.to_colouring(f, 4)
    assert size == 2 * 4 + 6 * len(f) + 3 and len(edges) == 3 * 4 + 12 * len(f) + 3
    assert is_colourable(size, edges, 3) == (brute_force(f) is not None)


def test_colouring_of_an_unsatisfiable_formula():
    size, edges = reduce_col.to_colouring(EVERY, 3)
    assert not is_colourable(size, edges, 3)


@settings(max_examples=80, deadline=None)
@given(three_cnf)
def test_subset_sum(f):
    f = f[:4]
    assert subset_sums_to(*reduce_ss.to_subset_sum(f, 4)) == (brute_force(f) is not None)


def test_subset_sum_of_an_unsatisfiable_formula():
    assert not subset_sums_to(*reduce_ss.to_subset_sum(EVERY, 3))


def test_cook_levin_counts_and_windows():
    clauses, num, width, legal = cook_levin.formula("011", 3)
    assert (width, legal, len(num), len(clauses)) == (7, 193, 3_091, 18_009)
    # the accepting run of the output: every window it shows is legal
    rows = [("#", "q0", "0", "1", "1", "_", "#"), ("#", "0", "q0", "1", "1", "_", "#"),
            ("#", "0", "1", "q1", "1", "_", "#"), ("#", "0", "1", "1", "qa", "_", "#")]
    windows = cook_levin.legal_windows(7)
    for top, bottom in zip(rows, rows[1:]):
        assert bottom in cook_levin.successors(top)
        assert all((top[j:j + 3], bottom[j:j + 3]) in windows for j in range(5))


def test_dpll_agrees_with_brute_force():
    rng = random.Random(17)
    for _ in range(300):
        f = random_3cnf(5, rng.randrange(1, 25), rng)
        a = dpll(f)
        assert (a is None) == (brute_force(f) is None)
        if a is not None:
            full = {v: a.get(v, False) for v in range(1, 6)}
            assert satisfies(f, full)


def test_two_sat():
    rng = random.Random(18)
    for _ in range(500):
        n = rng.randrange(1, 6)
        f = [tuple(rng.choice((1, -1)) * rng.randrange(1, n + 1) for _ in range(2))
             for _ in range(rng.randrange(1, 9))]
        a = two_sat.solve(f, n)
        assert (a is None) == (brute_force([list(c) for c in f]) is None)
        if a is not None:
            assert satisfies(f, a)


def test_subset_dp():
    rng = random.Random(19)
    for _ in range(200):
        nums = [rng.randrange(1, 30) for _ in range(rng.randrange(1, 7))]
        t = rng.randrange(0, 80)
        assert subset_dp.dp_cells(nums, t)[0] == subset_sums_to(nums, t)


@settings(max_examples=150, deadline=None)
@given(three_cnf)
def test_exercise_5_clique(f):
    sat = brute_force(f) is not None
    for build, must_hold in ((ex5_clique.fixed, True), (ex5_clique.buggy, False)):
        vertices, edges, k = build(f)
        n = len(vertices)
        present = set(edges)
        complement = [e for e in itertools.combinations(range(n), 2) if e not in present]
        if must_hold:
            assert has_independent_set(n, complement, k) == sat


def test_exercise_5_buggy_is_wrong_on_an_unsatisfiable_formula():
    vertices, edges, k = ex5_clique.buggy(EVERY)
    present = set(edges)
    complement = [e for e in itertools.combinations(range(len(vertices)), 2)
                  if e not in present]
    assert has_independent_set(len(vertices), complement, k)  # claims satisfiable


def test_exercise_6_colouring_to_sat():
    rng = random.Random(20)
    for _ in range(100):
        n = rng.randrange(1, 6)
        edges = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < 0.6]
        clauses = ex6_col_to_sat.colouring_to_sat(n, edges)
        assert (brute_force(clauses) is not None) == is_colourable(n, edges, 3)
