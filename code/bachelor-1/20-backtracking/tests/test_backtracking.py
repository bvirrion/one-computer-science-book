"""Enumerations against itertools; queens, sudoku, subset sum and knapsack against
brute force; the exercises."""

import itertools
import random
import sys
from math import comb
from pathlib import Path

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

import enumerate as en  # noqa: E402
import knapsack_bb  # noqa: E402
import queens  # noqa: E402
import queens_symmetry  # noqa: E402
import subset_sum  # noqa: E402
import sudoku  # noqa: E402
from colouring import colour  # noqa: E402
from distinct_parts import distinct_parts  # noqa: E402
from queens_subtrees import subtree  # noqa: E402
from wordsearch import find  # noqa: E402


def test_enumerations():
    for n in range(7):
        items = list(range(n))
        assert sorted(map(tuple, en.subsets_binary(items))) == sorted(
            s for k in range(n + 1) for s in itertools.combinations(items, k))
        assert sorted(map(tuple, en.subsets(items))) == sorted(map(tuple, en.subsets_binary(items)))
        assert sorted(map(tuple, en.permutations(list(items)))) == sorted(
            itertools.permutations(items))
        a, seen = list(items), [tuple(items)]
        while en.next_permutation(a):
            seen.append(tuple(a))
        assert seen == list(itertools.permutations(items))
        for k in range(n + 1):
            got = [tuple(c) for c in en.combinations(items, k)]
            assert got == list(itertools.combinations(items, k)) and len(got) == comb(n, k)


def test_queens():
    for n in range(1, 9):
        assert queens.solve(n)[0] == len(queens_symmetry.solutions(n))
    for n in range(1, 7):  # the full tree, walked: one node per partial permutation
        walked = sum(len(list(itertools.permutations(range(n), k))) for k in range(n + 1))
        assert walked == queens.full_tree_nodes(n)


def test_sudoku():
    clues = sudoku.read_grid(CH / "listings" / "grid.txt")
    g = list(clues)
    assert sudoku.solve(g, {"nodes": 0})
    for i in range(81):
        assert clues[i] in (".", g[i])
        assert sudoku.candidates(g[:i] + ["."] + g[i + 1:], i) == {g[i]}


def test_subset_sum():
    for n in (8, 12):
        values = subset_sum.pages(n)
        brute = sum(1 for k in range(n + 1) for s in itertools.combinations(values, k)
                    if sum(s) == 1000)
        assert subset_sum.count(values, 1000, prune=True)[0] == brute
        assert subset_sum.count(values, 1000, prune=False) == (brute, 2 ** (n + 1) - 1)


def test_knapsack():
    rng = random.Random(3)
    for _ in range(30):
        things = [(rng.randint(1, 20), rng.randint(1, 30)) for _ in range(rng.randint(1, 10))]
        cap = rng.randint(0, 60)
        brute = max(sum(v for _, v in s) for k in range(len(things) + 1)
                    for s in itertools.combinations(things, k) if sum(w for w, _ in s) <= cap)
        assert knapsack_bb.best(things, cap, True)[0] == brute == knapsack_bb.best(things, cap, False)[0]


def test_exercises():
    def count_dp(n):  # partitions into distinct parts, by dynamic programming
        ways = [1] + [0] * n
        for part in range(1, n + 1):
            for m in range(n, part - 1, -1):
                ways[m] += ways[m - part]
        return ways[n]

    for n in range(1, 40):
        parts = list(distinct_parts(n))
        assert len(parts) == count_dp(n) and all(sum(p) == n and len(set(p)) == len(p)
                                                 for p in parts)
    grid = ["cat", "ore", "dog"]
    assert find(grid, "core") is not None and find(grid, "dog") == [(2, 0), (2, 1), (2, 2)]
    assert find(grid, "cac") is None and find(grid, "god") is not None
    k4 = [(a, b) for a in range(4) for b in range(a + 1, 4)]
    assert colour(range(4), k4) is None and colour(range(4), k4, k=4) is not None
    rng = random.Random(1)
    for _ in range(20):
        edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if rng.random() < 0.4]
        c = colour(range(8), edges)
        brute = any(all(t[a] != t[b] for a, b in edges)
                    for t in itertools.product(range(3), repeat=8))
        assert (c is not None) == brute
        assert c is None or all(c[a] != c[b] for a, b in edges)


def test_queens_subtrees_and_friendships():
    for n in range(1, 9):
        sizes = [subtree(n, c) for c in range(n)]
        assert 1 + sum(sizes) == queens.solve(n)[1] and sizes == sizes[::-1]
    assert [subtree(6, c) for c in range(3)] == [22, 29, 25]
    import csv
    with open(subset_sum.TOWN / "friendships.csv", newline="") as f:
        edges = [(int(r["person_a"]), int(r["person_b"])) for r in csv.DictReader(f)]
    people = sorted({v for e in edges for v in e})
    c = colour(people, edges)
    assert c is not None and all(c[a] != c[b] for a, b in edges)
    assert colour(people, edges, k=2) is None
