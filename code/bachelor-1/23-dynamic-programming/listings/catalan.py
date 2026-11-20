"""catalan.py: the number of ways to parenthesise a product of n matrices."""

from functools import cache
from math import comb


@cache  # memoisation by the standard library: one call per n
def ways(n):
    """P(1) = 1, P(n) = sum over the last split k of P(k) P(n - k)."""
    if n == 1:
        return 1
    return sum(ways(k) * ways(n - k) for k in range(1, n))


if __name__ == "__main__":
    for n in (2, 3, 5, 10, 20):
        catalan = comb(2 * n - 2, n - 1) // n
        print(f"{n:2} matrices: {ways(n)} orders; Catalan C({n - 1}) = {catalan}")
