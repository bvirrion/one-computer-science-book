"""recurrences.py: four recurrences computed exactly, against their closed forms."""

from functools import cache


@cache
def search(n):  # T(1) = 0, T(n) = T(n/2) + 1
    return 0 if n == 1 else search(n // 2) + 1


@cache
def merge(n):  # T(1) = 0, T(n) = 2T(n/2) + n
    return 0 if n == 1 else 2 * merge(n // 2) + n


@cache
def three(n):  # T(1) = 1, T(n) = 3T(n/2) + n
    return 1 if n == 1 else 3 * three(n // 2) + n


@cache
def four(n):  # T(1) = 1, T(n) = 4T(n/2) + n
    return 1 if n == 1 else 4 * four(n // 2) + n


print(f"{'n':>5} {'T1':>3} {'T2':>6} {'T3':>7} {'T4':>8}   closed forms")
for k in range(0, 11, 2):
    n = 2**k
    closed = (k, n * k, 3 * 3**k - 2 * n, 2 * n * n - n)  # 3^k = n^(log2 3)
    values = (search(n), merge(n), three(n), four(n))
    assert values == closed
    t1, t2, t3, t4 = values
    print(f"{n:5d} {t1:3d} {t2:6d} {t3:7d} {t4:8d}   all equal")
