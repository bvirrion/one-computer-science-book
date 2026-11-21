"""exo_lzw_bound.py: the i-th code of LZW never stands for more than i letters."""
import random
from math import isqrt

from lzw import encode


def lengths(data):
    """How many letters each code of encode(data) stands for, in order."""
    log = []
    codes = encode(data, log)
    first = [len(word) - 1 for _, word in log]  # an entry: a code's word, one letter
    return first + [len(data) - sum(first)] if codes else []


def bound(n):  # the least c with c(c + 1)/2 >= n
    c = (isqrt(8 * n + 1) - 1) // 2
    return c if c * (c + 1) // 2 >= n else c + 1


rng = random.Random(7)
texts = [bytes(rng.choice(b"ab") for _ in range(rng.randrange(1, 200)))
         for _ in range(2000)]
texts += [b"a" * n for n in range(1, 200)]
assert all(k <= i for t in texts for i, k in enumerate(lengths(t), start=1))
assert all(len(encode(t)) >= bound(len(t)) for t in texts)
print(f"{len(texts)} texts: the i-th code covers at most i letters;"
      " no text beats the bound")
long = [t for t in texts[:2000] if len(t) >= 100]
gap = min(len(encode(t)) - bound(len(t)) for t in long)
print(f"{len(long)} random texts of 100 letters or more: {gap} or more codes above it")
print(f"a^n meets it: n = 100, {len(encode(b'a' * 100))} codes, bound {bound(100)}")
