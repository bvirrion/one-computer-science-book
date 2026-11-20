"""Greedy rules against exhaustive search, Huffman against all code trees, the exercises."""

import itertools
import random
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

import coins  # noqa: E402
import encode_decode  # noqa: E402
import huffman  # noqa: E402
import intervals  # noqa: E402
import knapsack_greedy  # noqa: E402
import partition_rooms  # noqa: E402
import penalties  # noqa: E402
from canonical import canonical  # noqa: E402
from lateness import brute, earliest_deadline, max_lateness  # noqa: E402
from platforms import platforms  # noqa: E402


def test_intervals_all_small():
    shapes = [(s, e) for s in range(5) for e in range(s + 1, 6)]
    for k in range(1, 5):
        for talks in itertools.combinations(shapes, k):
            got = intervals.greedy(list(talks), "earliest finish")
            assert len(got) == intervals.optimum(list(talks))
            assert all(not intervals.overlap(a, b) for a, b in itertools.combinations(got, 2))


def test_rooms():
    rng = random.Random(1)
    for _ in range(200):
        talks = intervals.random_talks(rng, rng.randint(1, 30))
        assignment = partition_rooms.rooms(talks)
        assert len(set(assignment.values())) == partition_rooms.max_overlap(talks)
        for a, b in itertools.combinations(assignment, 2):
            assert assignment[a] != assignment[b] or not intervals.overlap(a, b)


def test_penalties():
    rng = random.Random(2)
    for _ in range(300):
        tasks = [(rng.randint(1, 5), rng.randint(1, 20)) for _ in range(rng.randint(0, 8))]
        on_time = penalties.greedy(tasks)
        order = penalties.schedule(on_time, tasks)
        assert sorted(order) == sorted(tasks)
        assert all(order[i][0] >= i + 1 for i in range(len(on_time)))  # on time indeed
        assert sum(p for _, p in tasks) - sum(p for _, p in on_time) == \
            penalties.best_penalty(tasks)


def full_tree_depths(n, limit):
    """Every multiset of n leaf depths of a full binary tree (sum of 2^-d equal to 1)."""
    for depths in itertools.combinations_with_replacement(range(1, limit + 1), n):
        if sum(Fraction(1, 2**d) for d in depths) == 1:
            yield depths


def test_huffman_optimal():
    rng = random.Random(3)
    for _ in range(150):
        n = rng.randint(2, 6)
        freq = {chr(97 + i): rng.randint(1, 30) for i in range(n)}
        code = huffman.codewords(huffman.huffman_tree(freq))
        cost = sum(freq[s] * len(code[s]) for s in freq)
        f = sorted(freq.values(), reverse=True)
        best = min(sum(x * d for x, d in zip(f, sorted(ds))) for ds in full_tree_depths(n, n - 1))
        assert cost == best
        words = list(code.values())
        assert not any(a != b and b.startswith(a) for a in words for b in words)
        assert sum(Fraction(1, 2 ** len(w)) for w in words) == 1


def test_round_trip():
    text = huffman.catalogue()
    tree = huffman.huffman_tree(Counter(text))
    code = huffman.codewords(tree)
    assert sum(Counter(text)[s] * len(code[s]) for s in code) == 5993
    rng = random.Random(4)
    for _ in range(50):
        sample = "".join(rng.choice(text) for _ in range(rng.randint(0, 40)))
        assert encode_decode.decode(encode_decode.encode(sample, code), tree) == sample


def test_coins():
    for c in (2, 3, 5, 10):
        system = [c**i for i in range(4)]
        best = coins.fewest_coins(600, system)
        assert all(len(coins.greedy_change(a, system)) == best[a] for a in range(601))
    assert len(coins.greedy_change(6, [1, 3, 4])) == 3 and coins.fewest_coins(6, [1, 3, 4])[6] == 2


def test_knapsack():
    rng = random.Random(5)
    for _ in range(100):
        items = [(rng.randint(1, 10), rng.randint(1, 20)) for _ in range(rng.randint(1, 8))]
        cap = rng.randint(0, 30)
        brute_best = max(sum(v for _, v in s) for k in range(len(items) + 1)
                         for s in itertools.combinations(items, k)
                         if sum(w for w, _ in s) <= cap)
        assert knapsack_greedy.optimum(items, cap) == brute_best
        assert knapsack_greedy.greedy(items, cap) <= brute_best


def test_exercises():
    rng = random.Random(6)
    for _ in range(200):
        trains = []
        for _ in range(rng.randint(1, 12)):
            a = rng.randint(0, 50)
            trains.append((a, a + rng.randint(0, 10)))
        present = max(sum(a <= t <= d for a, d in trains) for t in range(70))
        assert platforms(trains) == present
    for _ in range(100):
        n = rng.randint(1, 8)
        freq = {chr(97 + i): rng.randint(1, 40) for i in range(n)}
        lengths = {s: len(w) for s, w in huffman.codewords(huffman.huffman_tree(freq)).items()}
        code = canonical(lengths)
        assert {s: len(w) for s, w in code.items()} == lengths
        words = list(code.values())
        assert not any(a != b and b.startswith(a) for a in words for b in words)
    for _ in range(100):
        tasks = [(rng.randint(1, 5), rng.randint(0, 15)) for _ in range(rng.randint(1, 6))]
        assert max_lateness(earliest_deadline(tasks)) == brute(tasks)
