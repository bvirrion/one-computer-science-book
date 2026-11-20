"""karatsuba_timing.py: microseconds per product of two random n-digit numbers,
school method against Karatsuba with three cutoffs (best of 5 runs)."""

import random
import time

from digits import school, to_digits
from karatsuba import karatsuba


def us(f, a, b):
    best = float("inf")
    for _ in range(5):
        t = time.perf_counter()
        f(a, b)
        best = min(best, time.perf_counter() - t)
    return 1e6 * best


def main():
    rng = random.Random(21)
    cutoffs = (1, 8, 32)
    head = "".join(f" {'cutoff ' + str(c):>10}" for c in cutoffs)
    print(f"{'n':>5} {'school':>9}" + head)
    for k in range(4, 12):
        n = 2**k
        a = to_digits(rng.randrange(10**n), n)
        b = to_digits(rng.randrange(10**n), n)
        row = [us(school, a, b)]
        row += [us(lambda x, y, c=c: karatsuba(x, y, c), a, b) for c in cutoffs]
        print(f"{n:5} {row[0]:9.0f}" + "".join(f" {t:10.0f}" for t in row[1:]))


if __name__ == "__main__":
    main()
