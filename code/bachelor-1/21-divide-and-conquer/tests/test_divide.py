"""Karatsuba against Python's *, closest pair and selection against brute force,
the dichotomy against a scan, meet in the middle against a count by sums; the exercises."""

import itertools
import random
import sys
from collections import Counter

from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

CH = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(CH / "listings"), str(CH / "exercises")]

import closest_pair  # noqa: E402
import digits  # noqa: E402
import meet_middle  # noqa: E402
import segments  # noqa: E402
import selection  # noqa: E402
from four_sum import four_sum  # noqa: E402
from inversions import sort_count  # noqa: E402
from karatsuba import karatsuba, multiply  # noqa: E402
from majority import majority  # noqa: E402
from max_subarray import best, kadane  # noqa: E402
from skyline import skyline  # noqa: E402


@settings(max_examples=200, deadline=None)
@given(st.integers(0, 10**80), st.integers(0, 10**80), st.sampled_from([1, 2, 4, 16]))
def test_karatsuba(x, y, cutoff):
    assert multiply(x, y) == x * y == multiply(x, y, "school")
    assert multiply(x, y, cutoff=cutoff) == x * y


def test_karatsuba_count():
    for k in range(9):
        for cutoff in (1, 2, 4):
            a = digits.to_digits(10**2**k - 1, 2**k)
            digits.products = 0
            karatsuba(a, a, cutoff)
            j = min(k, cutoff.bit_length() - 1)  # cutoff = 2^j
            assert digits.products == 3 ** (k - j) * 4**j


def test_inversions():
    rng = random.Random(1)
    for n in range(30):
        a = [rng.randint(0, 9) for _ in range(n)]
        brute = sum(a[i] > a[j] for i in range(n) for j in range(i + 1, n))
        assert sort_count(a) == (sorted(a), brute)


def test_closest():
    rng = random.Random(2)
    for n in (2, 3, 4, 5, 7, 20, 100):
        for _ in range(20):
            pts = list({(rng.randint(0, 50), rng.randint(0, 50)) for _ in range(n)})
            if len(pts) >= 2:
                assert closest_pair.closest(pts) == closest_pair.brute(pts)
    town = closest_pair.places()
    assert round(closest_pair.closest(list(town))) == 405


def test_selection():
    rng = random.Random(3)
    for n in (1, 2, 5, 6, 11, 50, 200):
        for _ in range(10):
            a = [rng.randint(0, 20) for _ in range(n)]
            k = rng.randrange(n)
            want = sorted(a)[k]
            assert selection.quickselect(a, k) == want
            assert selection.quickselect(a, k, random.Random(k)) == want
            assert selection.mom_select(a, k) == want


def test_segments():
    rng = random.Random(4)
    for _ in range(50):
        xs = sorted(rng.sample(range(200), rng.randint(1, 15)))
        for k in range(1, 5):
            scan = next(length for length in range(201) if segments.covers(xs, k, length))
            assert segments.smallest_length(xs, k)[0] == scan


def test_meet_middle():
    for n in (10, 16, 22):
        values = meet_middle.pages(n)
        ways = Counter({0: 1})  # number of subsets with each sum, item by item
        for v in values:
            new = Counter(ways)
            for s, c in ways.items():
                new[s + v] += c
            ways = new
        assert meet_middle.count(values, 1000)[0] == ways[1000]
    values = [3, 5, 2, 8]
    assert meet_middle.count(values, 10)[0] == sum(
        1 for k in range(5) for s in itertools.combinations(values, k) if sum(s) == 10)


def test_exercises():
    rng = random.Random(5)
    for _ in range(200):
        a = [rng.randint(-10, 10) for _ in range(rng.randint(1, 30))]
        assert best(a) == kadane(a) == max(sum(a[i:j]) for i in range(len(a))
                                            for j in range(i + 1, len(a) + 1))
        b = [rng.randint(0, 2) for _ in range(rng.randint(1, 15))]
        top, c = Counter(b).most_common(1)[0]
        assert majority(b) == (top if 2 * c > len(b) else None)
    for _ in range(100):
        bs = [(x, x + rng.randint(1, 5), rng.randint(1, 6))
              for x in (rng.randint(0, 20) for _ in range(rng.randint(1, 6)))]
        outline = skyline(bs)
        for x in range(30):  # the outline's height at x + 0.5 is the highest building there
            h = max((b[2] for b in bs if b[0] <= x < b[1]), default=0)
            last = [hh for xx, hh in outline if xx <= x]
            assert (last[-1] if last else 0) == h
        assert all(outline[i][1] != outline[i + 1][1] for i in range(len(outline) - 1))
    for _ in range(100):
        a = [rng.randint(-9, 9) for _ in range(rng.randint(0, 9))]
        t = rng.randint(-15, 15)
        r = four_sum(a, t)
        exists = any(sum(q) == t for q in itertools.combinations(a, 4))
        assert (r is not None) == exists
        assert r is None or (sum(a[i] for i in r) == t and list(r) == sorted(set(r)))
