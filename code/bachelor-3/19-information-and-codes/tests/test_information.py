import itertools
import math
import random
import sys
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE / "listings"), str(HERE / "exercises")]

import bsc  # noqa: E402
import capacity  # noqa: E402
import crc_poly  # noqa: E402
import ex5_syndrome  # noqa: E402
import ex6_hamming15  # noqa: E402
import hamming74  # noqa: E402
import kraft  # noqa: E402
from entropy import entropy, frequencies  # noqa: E402
from huffman_vs_h import blocks, huffman_lengths  # noqa: E402
from source import catalogue_text  # noqa: E402

dists = st.lists(st.floats(0.01, 1.0), min_size=2, max_size=12).map(
    lambda w: [x / sum(w) for x in w])


@given(dists)
def test_entropy_at_most_log_n_and_gibbs(p):
    n = len(p)
    assert entropy(p) <= math.log2(n) + 1e-9
    q = [1 / n] * n
    assert sum(a * math.log2(1 / b) for a, b in zip(p, q)) >= entropy(p) - 1e-9


def test_entropy_of_the_catalogue():
    f = frequencies(catalogue_text())
    assert len(catalogue_text()) == 1437 and len(f) == 23
    assert abs(entropy(f.values()) - 3.9904) < 1e-4


@given(st.lists(st.integers(1, 8), min_size=1, max_size=20))
def test_canonical_code_is_prefix_free(lengths):
    if kraft.kraft_sum(lengths) > 1:
        return
    words = kraft.code_from_lengths(lengths)
    assert sorted(map(len, words)) == sorted(lengths)
    assert kraft.is_prefix_free(words)


@given(dists)
def test_huffman_within_one_bit_of_entropy(p):
    probs = dict(enumerate(p))
    lengths = huffman_lengths(probs)
    assert kraft.kraft_sum(lengths.values()) == 1
    average = sum(probs[s] * lengths[s] for s in probs)
    assert entropy(p) - 1e-9 <= average < entropy(p) + 1


def test_blocks_are_a_distribution():
    f = frequencies(catalogue_text())
    assert abs(sum(blocks(f, 2).values()) - 1) < 1e-9


def test_repetition_and_capacity():
    assert math.isclose(bsc.repetition_error(3, 0.01), 3 * 0.01 ** 2 * 0.99 + 0.01 ** 3)
    assert capacity.h(0.5) == 1 and capacity.h(0) == 0
    assert math.isclose(capacity.h(0.1), capacity.h(0.9))


def test_hamming74_codewords_and_single_errors():
    codewords = {}
    for d in itertools.product((0, 1), repeat=4):
        c = hamming74.encode(list(d))
        assert hamming74.syndrome(c) == 0
        codewords[d] = c
        for i in range(7):
            r = list(c)
            r[i] ^= 1
            assert hamming74.syndrome(r) == i + 1
            assert hamming74.decode(r) == list(d)
    words = list(codewords.values())
    assert min(hamming74.distance(a, b) for a, b in itertools.combinations(words, 2)) == 3
    # perfect: the 16 balls of radius 1 hold 16 * 8 = 128 = 2^7 words
    balls = {tuple(c[:i] + [1 - c[i]] + c[i + 1:]) for c in words for i in range(7)}
    assert len(balls | {tuple(c) for c in words}) == 2 ** 7


def test_crc_detects_every_short_burst():
    rng = random.Random(0)
    for _ in range(20):
        c = crc_poly.encode(rng.getrandbits(24))
        assert crc_poly.remainder(c) == 0
        for length in range(1, crc_poly.R + 1):
            assert all(crc_poly.remainder(c ^ e) for e in crc_poly.bursts(length, 32))


def test_crc_burst_of_length_9_missed_once_per_position():
    patterns = list(crc_poly.bursts(9, 32))
    missed = [e for e in patterns if crc_poly.remainder(e) == 0]
    assert len(missed) == 24 and all(e >> (e & -e).bit_length() - 1 == crc_poly.G
                                     for e in missed)


def test_exercise_5():
    d = [1, 0, 1, 1]
    r = hamming74.encode(d)
    r[2] ^= 1  # position 3: syndrome 011 read as 110
    assert ex5_syndrome.buggy_decode(r) != d
    for d in itertools.product((0, 1), repeat=4):
        for i in range(7):
            r = hamming74.encode(list(d))
            r[i] ^= 1
            assert ex5_syndrome.fixed_decode(r) == list(d)


def test_exercise_6_all_single_errors():
    rng = random.Random(6)
    for _ in range(50):
        d = [rng.randrange(2) for _ in range(11)]
        c = ex6_hamming15.encode15(d)
        assert len(c) == 15 and ex6_hamming15.syndrome15(c) == 0
        assert ex6_hamming15.decode15(c) == d
        for i in range(15):
            r = list(c)
            r[i] ^= 1
            assert ex6_hamming15.decode15(r) == d
