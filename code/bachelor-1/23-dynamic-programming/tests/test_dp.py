"""Edit distance against brute force and its metric properties; knapsack, subset sum,
chain and LIS against exhaustive search; the exercises."""

import itertools
import random
import sys
from functools import cache
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

import catalan  # noqa: E402
import chain  # noqa: E402
import edit_distance  # noqa: E402
import fib_memo  # noqa: E402
import knapsack  # noqa: E402
import lis  # noqa: E402
import spell  # noqa: E402
import subset_sum_dp  # noqa: E402
from edit_two_rows import distance  # noqa: E402
from palindrome import longest_palindrome  # noqa: E402
from stairs import climbs  # noqa: E402
from weighted_intervals import best_weight  # noqa: E402

words = st.text(alphabet="abc", max_size=6)


def brute_edit(a, b):
    """Breadth-first search over words: the fewest single-letter edits from a to b."""
    seen, frontier, steps = {a}, {a}, 0
    while b not in frontier:
        nxt = set()
        for w in frontier:
            for i in range(len(w) + 1):
                for c in "abc":
                    nxt.add(w[:i] + c + w[i:])
                    if i < len(w):
                        nxt.add(w[:i] + c + w[i + 1:])
                if i < len(w):
                    nxt.add(w[:i] + w[i + 1:])
        frontier = {w for w in nxt if w not in seen and len(w) <= 7}
        seen |= frontier
        steps += 1
    return steps


@settings(max_examples=150, deadline=None)
@given(words, words)
def test_edit_distance(a, b):
    d = edit_distance.table(a, b)
    assert d[-1][-1] == distance(a, b)
    if len(a) + len(b) <= 7:  # small enough for the search over all words
        assert d[-1][-1] == brute_edit(a, b)
    top, bottom = edit_distance.alignment(a, b, d)
    assert top.replace("-", "") == a and bottom.replace("-", "") == b
    assert sum(x != y for x, y in zip(top, bottom)) == d[-1][-1]


@settings(max_examples=200, deadline=None)
@given(words, words, words)
def test_metric(a, b, c):
    assert (distance(a, b) == 0) == (a == b)
    assert distance(a, b) == distance(b, a)
    assert distance(a, c) <= distance(a, b) + distance(b, c)


def test_fib_and_catalan():
    assert [fib_memo.fib_table(n) for n in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    for n in range(1, 12):
        fib_memo.calls = 0
        fib_memo.fib_naive(n)
        assert fib_memo.calls == 2 * fib_memo.fib_table(n + 1) - 1
        fib_memo.calls = 0
        fib_memo.fib_memo(n)
        assert fib_memo.calls == max(1, 2 * n - 1)
    assert [catalan.ways(n) for n in range(1, 8)] == [1, 1, 2, 5, 14, 42, 132]


def test_chain():
    rng = random.Random(1)

    @cache
    def brute(dims, i, j):
        if i == j:
            return 0
        return min(brute(dims, i, k) + brute(dims, k + 1, j) + dims[i] * dims[k + 1] * dims[j + 1]
                   for k in range(i, j))

    for _ in range(50):
        dims = tuple(rng.randint(1, 30) for _ in range(rng.randint(2, 8)))
        cost, split = chain.chain_order(list(dims))
        assert cost[0][-1] == brute(dims, 0, len(dims) - 2)


def test_knapsack_and_subset_sum():
    rng = random.Random(2)
    for _ in range(100):
        items = [(rng.randint(1, 10), rng.randint(1, 30)) for _ in range(rng.randint(0, 8))]
        cap = rng.randint(0, 25)
        best = knapsack.knapsack(items, cap)
        brute = max(sum(v for _, v in s) for k in range(len(items) + 1)
                    for s in itertools.combinations(items, k) if sum(w for w, _ in s) <= cap)
        assert best[-1][cap] == brute
        take = knapsack.chosen(items, best, cap)
        assert sum(items[i][0] for i in take) <= cap
        assert sum(items[i][1] for i in take) == brute
        values = [rng.randint(1, 9) for _ in range(rng.randint(0, 10))]
        t = rng.randint(0, 30)
        assert subset_sum_dp.count(values, t) == sum(
            1 for k in range(len(values) + 1)
            for s in itertools.combinations(values, k) if sum(s) == t)


def test_lis():
    rng = random.Random(3)
    for _ in range(200):
        a = [rng.randint(0, 9) for _ in range(rng.randint(0, 10))]
        brute = max((k for k in range(len(a) + 1) for s in itertools.combinations(a, k)
                     if all(x < y for x, y in zip(s, s[1:]))), default=0)
        best = lis.lis_table(a)
        assert len(best) == lis.lis_patience(a) == brute
        assert all(x < y for x, y in zip(best, best[1:]))
        it = iter(a)
        assert all(x in it for x in best)  # a subsequence of a


def test_spell():
    books = spell.titles()
    pivots = books[:4]
    to_pivot = {t: [distance(t, p) for p in pivots] for t in books}
    rng = random.Random(4)
    for _ in range(20):
        t = list(rng.choice(books))
        for _ in range(rng.randint(0, 4)):
            t[rng.randrange(len(t))] = rng.choice("abcdefghijklmnopqrstuvwxyz ")
        q = "".join(t)
        (d, _), _ = spell.nearest_pruned(q, books, pivots, to_pivot)
        assert d == spell.nearest_brute(q, books)[0]


def test_exercises():
    rng = random.Random(5)
    for _ in range(100):
        talks = []
        for _ in range(rng.randint(0, 8)):
            s = rng.randint(0, 20)
            talks.append((s, s + rng.randint(1, 8), rng.randint(1, 10)))
        brute = max(sum(w for _, _, w in c) for k in range(len(talks) + 1)
                    for c in itertools.combinations(talks, k)
                    if all(x[1] <= y[0] or y[1] <= x[0] for x, y in itertools.combinations(c, 2)))
        assert best_weight(talks) == brute
    assert climbs(10, [1, 2]) == 89 and climbs(4, [1, 3]) == 3 and climbs(0, [2]) == 1
    for _ in range(100):
        s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 10)))
        brute = max((k for k in range(len(s) + 1) for c in itertools.combinations(s, k)
                     if list(c) == list(c)[::-1]), default=0)
        assert longest_palindrome(s) == brute
