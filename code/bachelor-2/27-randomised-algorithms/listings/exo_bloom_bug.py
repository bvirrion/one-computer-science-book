"""exo_bloom_bug.py: k positions h(x), h(x) + 1, ..., h(x) + k - 1 from one function,
against k independent functions."""
import random

from bloom import Bloom
from universal_hash import draw


class Consecutive(Bloom):
    def __init__(self, m, k, rng):
        self.bits = bytearray(m)
        h = draw(m, rng)
        self.hashes = [lambda x, i=i: (h(x) + i) % m for i in range(k)]


rng = random.Random(6)
n, m, k = 1000, 8000, 6
keys = rng.sample(range(10**9), n + 100_000)
for cls in [Bloom, Consecutive]:
    f = cls(m, k, rng)
    for x in keys[:n]:
        f.add(x)
    rate = sum(x in f for x in keys[n:]) / 100_000
    print(f"{cls.__name__:11} k = {k}: {sum(f.bits)} bits set,",
          f"false positives {rate:.4f}")
