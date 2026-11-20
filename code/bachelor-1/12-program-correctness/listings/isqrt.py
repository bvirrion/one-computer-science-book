"""isqrt.py: the integer square root, by bisection and by Newton's method.
Specification: for n >= 0, return r with r * r <= n < (r + 1) * (r + 1)."""

import math


def isqrt_bisect(n):
    lo, hi = 0, n + 1  # invariant: lo * lo <= n < hi * hi
    steps = 0
    while hi - lo > 1:  # variant: hi - lo
        mid = (lo + hi) // 2  # lo < mid < hi
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid
        steps += 1
    return lo, steps


def isqrt_newton(n):
    if n == 0:
        return 0, 0
    r = n  # invariant: r >= the integer square root of n
    steps = 0
    while r * r > n:  # variant: r, which decreases strictly
        r = (r + n // r) // 2
        steps += 1
    return r, steps


if __name__ == "__main__":
    print(f"{'n':>22} {'root':>11} {'bisection':>9} {'ceil(log2(n+1))':>15}",
          f"{'Newton':>6}")
    for n in [0, 1, 2, 15, 16, 17, 99, 10**6, 2**32 - 1, 2**32, 10**18, 2**64 - 1]:
        (r1, s1), (r2, s2) = isqrt_bisect(n), isqrt_newton(n)
        assert r1 == r2 == math.isqrt(n)
        bound = math.ceil(math.log2(n + 1))
        print(f"{n:22d} {r1:11d} {s1:9d} {bound:15d} {s2:6d}")
