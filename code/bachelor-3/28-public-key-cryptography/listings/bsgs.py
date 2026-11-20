"""bsgs.py -- baby-step giant-step: discrete logarithms in subgroups of prime order q
from 2^20 to 2^36, counting the group operations each one takes."""

import math
import random

from groups import subgroup


def bsgs(g, h, p, q):
    """Return x with g^x = h mod p, 0 <= x < q, and the number of multiplications."""
    m = math.isqrt(q - 1) + 1  # m = ceil(sqrt(q)), so x = i*m + j with i, j < m
    baby, e = {}, 1
    for j in range(m):  # baby steps: g^0, g^1, ..., g^(m-1)
        baby.setdefault(e, j)
        e = e * g % p
    step = pow(g, -m, p)  # g^(-m)
    gamma = h
    for i in range(m):  # giant steps: h, h g^-m, h g^-2m, ...
        if gamma in baby:
            return i * m + baby[gamma], m + i
        gamma = gamma * step % p
    raise ValueError("h is not a power of g")


if __name__ == "__main__":
    rng = random.Random(28)
    print("bits of q  2*sqrt(q)  most steps  mean steps  mean/sqrt(q)  (20 logs each)")
    for bits in (20, 24, 28, 32, 36):
        p, q, g = subgroup(bits, 64, rng)
        counts = []
        for _ in range(20):
            x = rng.randrange(q)
            found, steps = bsgs(g, pow(g, x, p), p, q)
            assert found == x
            counts.append(steps)
        mean = sum(counts) / len(counts)
        print(
            f"{bits:9} {2 * math.isqrt(q):10,} {max(counts):11,} {mean:11,.0f}"
            f" {mean / math.sqrt(q):13.2f}"
        )
