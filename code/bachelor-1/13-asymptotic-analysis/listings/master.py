"""master.py: the case of the master theorem for T(n) = a T(n/b) + n^k."""

from math import log


def master(a, b, k):
    """For a >= 1, b >= 2, k >= 0: the case, the order of T, and a function g
    with T in Theta(g)."""
    if a < b**k:
        return "root", f"n^{k}", lambda n: n**k
    if a == b**k:
        return "even", f"n^{k} log n", lambda n: n**k * log(n, b)
    e = log(a, b)
    return "leaves", f"n^{e:.3f}", lambda n: n**e


def exact(a, b, k, n):
    """T(1) = 1 and T(n) = a T(n/b) + n^k, for n a power of b."""
    return 1 if n == 1 else a * exact(a, b, k, n // b) + n**k


examples = [("binary search", 1, 2, 0), ("merge sort", 2, 2, 1),
            ("Karatsuba", 3, 2, 1), ("eight products", 8, 2, 2),
            ("Strassen", 7, 2, 2), ("square at the root", 2, 2, 2)]
print(f"{'':>18}  a b k  {'case':>6}  {'Theta':<11} T/g at 2^10, 2^20")
for name, a, b, k in examples:
    case, order, g = master(a, b, k)
    r1, r2 = (exact(a, b, k, n) / g(n) for n in (2**10, 2**20))
    print(f"{name:>18}  {a} {b} {k}  {case:>6}  {order:<11} {r1:6.3f} {r2:6.3f}")
