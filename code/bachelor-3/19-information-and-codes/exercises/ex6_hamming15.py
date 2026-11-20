"""ex6_hamming15.py -- the Hamming (15,11) code: parity bits at positions 1, 2, 4 and 8,
data at the other eleven; the syndrome of a single error is its position."""

DATA = [j for j in range(1, 16) if j & (j - 1)]  # not a power of two


def encode15(d):
    assert len(d) == 11
    c = [0] * 16
    for pos, bit in zip(DATA, d):
        c[pos] = bit
    for i in range(4):
        c[1 << i] = sum(c[j] for j in DATA if j >> i & 1) % 2
    return c[1:]


def syndrome15(word):
    s = 0
    for j, bit in enumerate(word, start=1):
        if bit:
            s ^= j  # XOR of the positions of the 1s
    return s


def decode15(word):
    word = list(word)
    s = syndrome15(word)
    if s:
        word[s - 1] ^= 1
    return [word[pos - 1] for pos in DATA]
