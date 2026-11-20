import functools
import itertools
import math
import random
import subprocess
import sys
from collections import Counter
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
SHARED = HERE.parents[1] / "shared"
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises"), str(SHARED / "town")]

import ex5_hash  # noqa: E402
import ex6_sortmerge  # noqa: E402
import ex11_twocol  # noqa: E402
import ex12_orders  # noqa: E402
import histogram  # noqa: E402
import joins  # noqa: E402
import overdue  # noqa: E402
import rewrite  # noqa: E402
import selinger  # noqa: E402
import town  # noqa: E402
from exec import Disk, Relation  # noqa: E402
from sort_ext import external_sort, formula  # noqa: E402


def as_set(rows):
    return sorted(tuple(sorted(r.items())) for r in rows)


@settings(max_examples=40, deadline=None)
@given(st.integers(1, 400), st.integers(3, 12))
def test_external_sort_cost_is_the_formula(n_pages, B):
    rng = random.Random(n_pages * 13 + B)
    rel = Relation({"k": rng.random()} for _ in range(10 * n_pages))
    disk = Disk()
    out, passes = external_sort(rel, lambda t: t["k"], B, disk)
    assert [t["k"] for t in out.rows()] == sorted(t["k"] for t in rel.rows())
    assert disk.io() == formula(n_pages, B)
    assert disk.reads == disk.writes == n_pages * passes


@settings(max_examples=30, deadline=None)
@given(st.integers(1, 60), st.integers(1, 30), st.integers(4, 12), st.integers(0, 99))
def test_joins_agree_and_cost_their_formulas(m, n, B, seed):
    rng = random.Random(seed)
    S = Relation({"k": j, "v": rng.random()} for j in range(10 * n))
    R = Relation({"i": i, "fk": rng.randrange(12 * n)} for i in range(10 * m))
    M, N, nr = len(R), len(S), 10 * m
    d = Disk()
    ref = as_set(joins.nested_loop(R, S, "fk", "k", d))
    assert d.io() == M + nr * N
    d = Disk()
    assert as_set(joins.block_nested_loop(R, S, "fk", "k", B, d)) == ref
    assert d.io() == M + math.ceil(M / (B - 2)) * N
    tree = joins.build_index(S, "k")
    d = Disk()
    out = joins.index_nested_loop(R, S, "fk", "k", tree, d)
    assert as_set(out) == ref
    assert d.io() == M + nr * tree.height() + len(out)
    d = Disk()
    assert as_set(joins.sort_merge(R, S, "fk", "k", B, d)) == ref
    assert d.io() == formula(M, B) + formula(N, B) + M + N
    d = Disk()
    assert as_set(joins.hash_join(R, S, "fk", "k", B, d)) == ref
    if min(M, N) <= B - 2:
        assert d.io() == M + N
    else:  # partitions end in part-filled pages: at most one more page per bucket
        assert 3 * (M + N) <= d.io() <= 3 * (M + N) + 4 * (B - 1)


def test_rewrite_and_overdue():
    sizes = []
    rows = rewrite.run(rewrite.QUERY, sizes)
    pushed = []
    assert as_set(rewrite.run(rewrite.push(rewrite.QUERY), pushed)) == as_set(rows)
    inter = [sum(n for nd, n in s if nd[0] != "table") for s in (sizes, pushed)]
    assert inter == [1331, 162] and len(rows) == 11
    got = []
    for plan in (overdue.plan_a, overdue.plan_b, overdue.plan_c):
        d = Disk()
        out = plan(d)
        got.append((len(out), d.reads, d.writes))
    assert got == [(109, 524, 120), (109, 155, 89), (109, 727, 33)]


def all_left_deep(sizes, preds, B=10):
    """Exhaustive: every order without cross products, every method per join."""
    best = math.inf
    for order in itertools.permutations(sorted(sizes)):
        states = [(0, sizes[order[0]], None)]
        ok = True
        for i, r in enumerate(order[1:], 1):
            ps = [preds[p] for p in preds if r in p and p - {r} <= set(order[:i])]
            if not ps:
                ok = False
                break
            new = []
            for cost, t, o in states:
                out = t * sizes[r] * math.prod(s for _, s in ps)
                for _, c, no in selinger.methods(
                    selinger.pages(t), selinger.pages(sizes[r]), o, ps[0][0], B
                ):
                    new.append((cost + c, out, no))
            states = new
        if ok:
            best = min(best, min(c for c, _, _ in states))
    return best


def test_selinger_against_exhaustive_search():
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randint(2, 5)
        sizes, preds = selinger.random_query(n, rng.choice(["chain", "star"]), rng)
        if rng.random() < 0.5:  # one join column for all: orders become interesting
            preds = {p: ("k", s) for p, (_, s) in preds.items()}
        exact = all_left_deep(sizes, preds)
        (with_orders, _, _), _ = ex12_orders.best_plan_orders(sizes, preds)
        (plain, _, _), _ = selinger.best_plan(sizes, preds)
        assert with_orders == exact <= plain
        if len({c for c, _ in preds.values()}) == len(preds):
            assert plain == exact
    (a, _, _), _ = selinger.best_plan(*ex12_orders.QUERY)
    (b, _, _), _ = ex12_orders.best_plan_orders(*ex12_orders.QUERY)
    assert (a, b) == (90, 70)


def count_bushy(n):
    """Join trees with n labelled leaves, counted by splitting the set of leaves."""

    @functools.lru_cache(None)
    def trees(k):
        if k == 1:
            return 1
        return sum(math.comb(k, i) * trees(i) * trees(k - i) for i in range(1, k))

    return trees(n)


def test_counting_plans():
    for n in range(1, 8):
        assert count_bushy(n) == math.factorial(2 * n - 2) // math.factorial(n - 1)


def test_estimates_and_exercises():
    rain = [w["rain_mm"] for w in town.load("weather")]
    ew, ed = histogram.equi_width(rain, 8), histogram.equi_depth(rain, 8)
    got = [
        round(histogram.estimate(h, lo, hi), 1)
        for lo, hi in ((0, 0), (1, 3), (10, 99))
        for h in (ew, ed)
    ]
    assert got == [21.8, 395.3, 358.2, 87.5, 27.3, 59.9]
    assert [ex11_twocol.two_column(3, 3), round(ex11_twocol.independent(3, 3), 1)] == [
        40,
        6.4,
    ]
    loans = town.load("loans")
    counts = Counter(t["member_id"] for t in loans)
    assert sum(c * c for c in counts.values()) == 3084  # ex 9: the true self-join
    assert round(400 * 400 / len(counts)) == 2667
    rng = random.Random(3)
    R = Relation({"a": rng.randrange(30), "r": i} for i in range(200))
    S = Relation({"b": rng.randrange(30), "s": i} for i in range(50))
    ref = as_set(joins.nested_loop(R, S, "a", "b", Disk()))
    costs = []
    for f in (ex5_hash.buggy_hash_join, ex5_hash.fixed_hash_join):
        d = Disk()
        assert as_set(f(R, S, "a", "b", 8, d)) == ref
        costs.append(d.io())
    assert costs == [85, 25]


@settings(max_examples=40, deadline=None)
@given(
    st.lists(st.integers(0, 8), max_size=60),
    st.lists(st.integers(0, 8), max_size=40),
    st.integers(3, 6),
)
def test_sort_merge_with_duplicates(ra, sb, B):
    R = Relation({"a": v, "r": i} for i, v in enumerate(ra))
    S = Relation({"b": v, "s": i} for i, v in enumerate(sb))
    ref = as_set(joins.nested_loop(R, S, "a", "b", Disk()))
    assert as_set(ex6_sortmerge.sort_merge_dup(R, S, "a", "b", B, Disk())) == ref


def test_ex4_plan_lines():
    out = subprocess.run(
        [
            sys.executable,
            str(SHARED / "sqlrun" / "sqlrun.py"),
            str(HERE / "exercises" / "ex4_plan.sql"),
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    lines = [
        ln.split("|")[4].strip()
        for ln in out.splitlines()
        if ln.startswith("| ") and ("SCAN" in ln or "SEARCH" in ln)
    ]
    assert lines == [
        "SCAN l",
        "SEARCH b USING INTEGER PRIMARY KEY (rowid=?)",
        "SCAN b",
        "SEARCH l USING INDEX loans_book (book_id=?)",
    ]


def test_solution_numbers():
    rain = [w["rain_mm"] for w in town.load("weather")]
    assert histogram.equi_width(rain, 8)[0] == (0.0, 2.5125, 568, 26)
    assert histogram.equi_depth(rain, 8)[4] == (0.0, 0.2, 91, 3)
    assert [formula(5000, 11), formula(5000, 101), formula(110, 11)] == [
        40_000,
        20_000,
        440,
    ]
    assert 2000 + math.ceil(2000 / 50) * 300 == 14_000  # ex 1
    assert 300 + math.ceil(300 / 50) * 2000 == 12_300
    d = Disk()  # problem 17: plan A's joins with the selection first
    cur = overdue.materialise(
        overdue.select(overdue.late, overdue.scan(overdue.T["loans"], d)), d
    )
    before = d.reads
    for col, table in overdue.KEYS:
        cur = overdue.materialise(
            joins.block_nested_loop(cur, overdue.T[table], col, col, overdue.B, d), d
        )
    assert d.reads - before == 137
    sizes = {"late_loans": 109, "books": 80, "members": 60, "people": 120}
    preds = {
        frozenset({"late_loans", "books"}): ("book_id", 1 / 80),
        frozenset({"late_loans", "members"}): ("member_id", 1 / 60),
        frozenset({"members", "people"}): ("person_id", 1 / 120),
    }
    assert all_left_deep(sizes, preds, B=5) == 162
    assert 3 * (11 + 6) + 3 * (11 + 12) + 3 * (11 + 8) == 177  # problem 20
