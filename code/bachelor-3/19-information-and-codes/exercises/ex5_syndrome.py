"""ex5_syndrome.py -- a Hamming (7,4) decoder whose syndrome reads the rows of H in the
wrong order. Find a single error it fails to correct, and fix it."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from hamming74 import DATA, H  # noqa: E402


def buggy_decode(word):
    word = list(word)
    s = sum((sum(h * w for h, w in zip(row, word)) % 2) << (2 - i)  # BUG: bit order
            for i, row in enumerate(H))
    if s:
        word[s - 1] ^= 1
    return [word[pos - 1] for pos in DATA]


def fixed_decode(word):
    word = list(word)
    s = sum((sum(h * w for h, w in zip(row, word)) % 2) << i for i, row in enumerate(H))
    if s:
        word[s - 1] ^= 1
    return [word[pos - 1] for pos in DATA]
