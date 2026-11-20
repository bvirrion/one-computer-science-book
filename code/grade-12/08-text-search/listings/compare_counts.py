"""Comparisons per text letter, naive and Horspool, on generated texts."""
import random

from horspool import horspool
from naive import search_naive

rng = random.Random(8)
n = 100_000
alphabets = [("26 letters", "abcdefghijklmnopqrstuvwxyz"), ("4 letters", "ACGT")]
for name, alphabet in alphabets:
    text = "".join(rng.choice(alphabet) for _ in range(n))
    for m in [4, 8, 16, 32]:
        start = rng.randrange(n - m)
        p = text[start:start + m]           # a pattern that occurs at least once
        found_n, naive_c = search_naive(text, p)
        found_h, hors_c = horspool(text, p)
        assert found_n == found_h
        print(f"{name}, m = {m:2}: naive {naive_c / n:5.2f} per letter,"
              f" Horspool {hors_c / n:5.2f}, found {len(found_h)}")
