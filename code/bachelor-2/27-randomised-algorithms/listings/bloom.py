"""bloom.py: a Bloom filter of m bits with k hash functions from the universal family;
the false-positive rate measured against the formula."""
import math
import random

from universal_hash import draw


class Bloom:
    def __init__(self, m, k, rng):
        self.bits = bytearray(m)
        self.hashes = [draw(m, rng) for _ in range(k)]

    def add(self, x):
        for h in self.hashes:
            self.bits[h(x)] = 1

    def __contains__(self, x):  # never wrong for a key added; sometimes for others
        return all(self.bits[h(x)] for h in self.hashes)


if __name__ == "__main__":
    rng = random.Random(5)
    n, m = 1000, 8000  # 8 bits per key
    keys = rng.sample(range(10**9), n + 100_000)
    members, others = keys[:n], keys[n:]
    print(f"n = {n} keys, m = {m} bits; 100,000 other keys queried")
    print(" k  measured  (1 - e^(-kn/m))^k")
    for k in range(1, 11):
        f = Bloom(m, k, rng)
        for x in members:
            f.add(x)
        assert all(x in f for x in members)
        rate = sum(x in f for x in others) / len(others)
        print(f"{k:2}  {rate:8.4f}  {(1 - math.exp(-k * n / m)) ** k:8.4f}")
    print(f"best k = (m/n) ln 2 = {m / n * math.log(2):.2f}")
