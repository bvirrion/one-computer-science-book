"""The weekend problem: the integer square root, by counting up and by halving."""
import math


def isqrt_linear(n):
    r, turns = 0, 0
    while (r + 1) * (r + 1) <= n:      # variant: n - r * r
        r, turns = r + 1, turns + 1
    return r, turns


def isqrt_halving(n):
    lo, hi, turns = 0, n + 1, 0
    while hi - lo > 1:                 # invariant: lo * lo <= n < hi * hi
        mid = (lo + hi) // 2
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid
        turns = turns + 1
    return lo, turns


for n in [0, 1, 15, 16, 17, 1000]:
    print(f"n = {n:4}: linear {isqrt_linear(n)}, halving {isqrt_halving(n)}")
N = 10**6
worst, first = 0, None
for n in range(N + 1):
    r, turns = isqrt_halving(n)
    assert r == math.isqrt(n)
    if turns > worst:
        worst, first = turns, n
print(f"0 <= n <= {N}: halving always right,"
      f" at most {worst} turns (first at n = {first})")
print(f"linear at n = {N}: {isqrt_linear(N)[1]} turns")
