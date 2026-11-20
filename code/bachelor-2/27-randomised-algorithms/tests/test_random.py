import itertools
import random
from collections import Counter
from fractions import Fraction
from math import gcd

from hypothesis import given, settings
from hypothesis import strategies as st

from bloom import Bloom
from exo_skiplist import SkipList
from karger import contract
from primality import fermat_passes, is_probable_prime, miller_rabin_passes
from quickselect import quickselect
from quicksort import first, quicksort, random_pivot, shuffle
from universal_hash import chains


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n**0.5) + 1))


@settings(max_examples=100, deadline=None)
@given(st.lists(st.integers(), unique=True), st.integers(0, 10**6))
def test_quicksort_sorts(a, seed):
    assert quicksort(a, random_pivot(random.Random(seed)), [0]) == sorted(a)
    assert sorted(shuffle(a, random.Random(seed))) == sorted(a)


def test_sorted_input_is_quadratic():
    count = [0]
    quicksort(list(range(50)), first, count)
    assert count[0] == 50 * 49 // 2


def test_expected_comparisons_exactly():
    """Average over every pivot choice, by the recurrence, against 2(n+1)H_n - 4n."""
    exp = [Fraction(0)] * 30
    for n in range(2, 30):
        exp[n] = n - 1 + sum(exp[i] + exp[n - 1 - i] for i in range(n)) / n
        H = sum(Fraction(1, k) for k in range(1, n + 1))
        assert exp[n] == 2 * (n + 1) * H - 4 * n


@settings(max_examples=100, deadline=None)
@given(st.lists(st.integers(), unique=True, min_size=1), st.data())
def test_quickselect(a, data):
    k = data.draw(st.integers(0, len(a) - 1))
    count = [0]
    assert quickselect(a, k, random.Random(k), count) == sorted(a)[k]
    assert count[0] <= len(a) * (len(a) - 1) // 2 + len(a)


def test_carter_wegman_universal_exhaustively():
    p, m = 31, 6
    for x, y in itertools.combinations(range(p), 2):
        same = sum((a * x + b) % p % m == (a * y + b) % p % m
                   for a in range(1, p) for b in range(p))
        assert Fraction(same, (p - 1) * p) <= Fraction(1, m)


def test_chains():
    assert chains([0, 5, 10, 3], lambda x: x % 5, 5) == [3, 0, 0, 1, 0]


def test_bloom_has_no_false_negative():
    rng = random.Random(1)
    f = Bloom(500, 4, rng)
    keys = rng.sample(range(10**6), 100)
    for x in keys:
        f.add(x)
    assert all(x in f for x in keys)


def test_primality_agrees_with_trial_division():
    rng = random.Random(2)
    for n in range(2, 3000):
        assert is_probable_prime(n, 20, rng) == is_prime(n)
    for n in [561, 1105, 1729, 2465, 2821, 6601]:  # Carmichael numbers
        assert not is_prime(n)
        assert all(fermat_passes(n, a) for a in range(2, n - 1) if gcd(a, n) == 1)
        liars = sum(miller_rabin_passes(n, a) for a in range(2, n - 1))
        assert liars <= (n - 3) / 4


def test_primes_pass_every_base():
    for n in [5, 7, 101, 1009, 7919]:
        assert all(miller_rabin_passes(n, a) for a in range(2, n - 1))


def brute_min_cut(vertices, edges):
    best = len(edges)
    for k in range(1, len(vertices)):
        for side in itertools.combinations(vertices, k):
            s = set(side)
            best = min(best, sum((u in s) != (v in s) for u, v in edges))
    return best


@settings(max_examples=60, deadline=None)
@given(st.lists(st.tuples(st.integers(0, 5), st.integers(0, 5)), min_size=1, max_size=12),
       st.integers(0, 1000))
def test_karger_cut_is_a_cut(edges, seed):
    edges = [(u, v) for u, v in edges if u != v]
    vertices = list(range(6))
    cut, side = contract(vertices, edges, random.Random(seed))
    assert 0 < len(side) < 6 or not edges
    assert sorted(cut) == sorted((u, v) for u, v in edges if (u in side) != (v in side))
    assert len(cut) >= brute_min_cut(vertices, edges)


def test_karger_finds_the_minimum_often():
    vertices = list("abcdefgh")
    edges = (list(itertools.combinations("abcd", 2))
             + list(itertools.combinations("efgh", 2)) + [("d", "e"), ("c", "f")])
    rng = random.Random(0)
    wins = sum(len(contract(vertices, edges, rng)[0]) == 2 for _ in range(3000))
    assert wins / 3000 >= 2 / (8 * 7)


def test_shuffles_exhaustively():
    n = 4
    good = Counter()
    for choices in itertools.product(*[range(i, n) for i in range(n)]):
        a = list(range(n))
        for i, j in enumerate(choices):
            a[i], a[j] = a[j], a[i]
        good[tuple(a)] += 1
    assert len(good) == 24 and set(good.values()) == {1}


@settings(max_examples=50, deadline=None)
@given(st.lists(st.integers(0, 1000), unique=True, min_size=1), st.integers(-5, 1005))
def test_skiplist_search(keys, q):
    s = SkipList(random.Random(len(keys)))
    for k in keys:
        s.insert(k)
    node, _ = s.search(q)
    below = [k for k in keys if k <= q]
    assert (node[0] if node else None) == (max(below) if below else None)
