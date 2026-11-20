"""collide.py: k strings of length L with the same polynomial hash
h(s) = sum s_i 31^(L-1-i) mod 2^64, built from the equal-hash blocks "Aa" and "BB"."""

from itertools import islice, product


def poly(s):
    h = 0
    for ch in s:
        h = (31 * h + ord(ch)) % 2**64
    return h


def colliding(k, length):
    """k distinct strings of the even length `length`, all with one hash value."""
    blocks = length // 2
    assert length % 2 == 0 and k <= 2**blocks
    return ["".join(p) for p in islice(product(["Aa", "BB"], repeat=blocks), k)]
