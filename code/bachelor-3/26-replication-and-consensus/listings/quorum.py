"""quorum.py -- N replicas, reads ask R of them and writes W. Each replica is down
independently with probability p. For each choice: do every read quorum and every
write quorum overlap, and how likely is a read or a write to find too few replicas?"""

from itertools import combinations, product
from math import comb


def overlap(n, r, w):
    nodes = range(n)
    return all(
        set(a) & set(b) for a in combinations(nodes, r) for b in combinations(nodes, w)
    )


def unavailable_exact(n, k, p):
    """Sum over all 2^n up/down states of those with fewer than k replicas up."""
    total = 0.0
    for state in product((True, False), repeat=n):
        up = sum(state)
        if up < k:
            total += (1 - p) ** up * p ** (n - up)
    return total


def unavailable_formula(n, k, p):
    """At least n - k + 1 replicas down: a binomial tail."""
    return sum(comb(n, d) * p**d * (1 - p) ** (n - d) for d in range(n - k + 1, n + 1))


if __name__ == "__main__":
    p = 0.01
    print(f"p = {p}")
    print(" N  R  W  R+W>N  overlap  read unavailable  write unavailable")
    for n, r, w in [(3, 2, 2), (5, 3, 3), (5, 2, 4), (5, 1, 5), (5, 2, 3), (5, 2, 2)]:
        ru, wu = unavailable_exact(n, r, p), unavailable_exact(n, w, p)
        assert abs(ru - unavailable_formula(n, r, p)) < 1e-15
        assert abs(wu - unavailable_formula(n, w, p)) < 1e-15
        print(
            f"{n:>2} {r:>2} {w:>2}  {str(r + w > n):<5}  {str(overlap(n, r, w)):<7}"
            f"  {ru:>16.3e}  {wu:>17.3e}"
        )
    print(f"N=5, W=3: exact {unavailable_exact(5, 3, p):.6e}, 10p^3 = {10 * p**3:.6e}")
    print(f"N=5, W=5: exact {unavailable_exact(5, 5, p):.6e}, 5p = {5 * p:.6e}")
