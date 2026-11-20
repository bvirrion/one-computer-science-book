"""hamming74.py -- the Hamming (7,4) code over GF(2). Positions 1 to 7; the parity bits
sit at 1, 2 and 4, and column j of the parity-check matrix is j written in binary, so
the syndrome of a single error is its position."""
import itertools
import random

H = [[(j >> i) & 1 for j in range(1, 8)] for i in range(3)]  # row i: bit i of 1..7
DATA = [3, 5, 6, 7]  # the positions of the four data bits


def encode(d):
    c = [0] * 8  # c[1..7]; c[0] unused
    for pos, bit in zip(DATA, d):
        c[pos] = bit
    for i in range(3):  # parity bit 2^i makes row i of H c even
        c[1 << i] = sum(c[j] for j in range(1, 8) if j >> i & 1 and j != 1 << i) % 2
    return c[1:]


def syndrome(word):
    """H times the word, mod 2, read as a binary number."""
    bits = [sum(h * w for h, w in zip(row, word)) % 2 for row in H]
    return sum(b << i for i, b in enumerate(bits))


def decode(word):
    word, s = list(word), syndrome(word)
    if s:
        word[s - 1] ^= 1  # a single error at position s
    return [word[pos - 1] for pos in DATA]


def distance(a, b):
    return sum(x != y for x, y in zip(a, b))


if __name__ == "__main__":
    codewords = [encode(d) for d in itertools.product((0, 1), repeat=4)]
    print("parity-check matrix:", *("".join(map(str, row)) for row in H))
    print("1011 ->", "".join(map(str, encode([1, 0, 1, 1]))))
    received = encode([1, 0, 1, 1])
    received[4] ^= 1
    print("received", "".join(map(str, received)), "syndrome", syndrome(received),
          "decoded", "".join(map(str, decode(received))))
    print(f"{len(codewords)} codewords, minimum distance",
          min(distance(a, b) for a, b in itertools.combinations(codewords, 2)))
    rng, p, n = random.Random(19), 0.01, 1_000_000
    plain = coded = 0
    for _ in range(n):
        d = [rng.randrange(2) for _ in range(4)]
        plain += any(rng.random() < p for _ in range(4))
        sent = [b ^ (rng.random() < p) for b in encode(d)]
        coded += decode(sent) != d
    print(f"p = {p}, {n:,} blocks of 4 bits: block errors {plain / n:.4%} uncoded, "
          f"{coded / n:.4%} with Hamming (7,4)")
    one_or_none = 0.99 ** 7 + 7 * 0.01 * 0.99 ** 6
    print(f"computed: {1 - 0.99 ** 4:.4%} and {1 - one_or_none:.4%}")
