"""Exercises of the chapter on the cost of an algorithm."""
import functools


def double_loop(n):                               # exercise 4
    count = 0
    for i in range(n):
        for _ in range(i):
            count += 1
    return count


def count_comparisons(sort, t):                   # exercise 5
    """Sort a copy of t with sort, and return how many < comparisons it made."""
    count = 0

    def less(a, b):
        nonlocal count
        count += 1
        return -1 if a < b else (1 if b < a else 0)

    sort_key = functools.cmp_to_key(less)
    sort([sort_key(v) for v in t])
    return count


def selection_count(n):                           # exercise 6
    count = 0
    for i in range(n):
        for _ in range(i + 1, n):
            count += 1
    return count


def has_duplicate(t):                             # exercise 9
    return any(t[i] == t[j] for i in range(len(t)) for j in range(i + 1, len(t)))


def h(n):                                         # exercise 11
    count = 0
    while n > 1:
        n //= 2
        count += 1
    return count


def binary_comparisons(n, x_index):               # exercise 12: three-way comparisons
    t = list(range(n))
    lo, hi, count = 0, n, 0
    while lo < hi:
        mid = (lo + hi) // 2
        count += 1
        if t[mid] == x_index:
            return count
        if t[mid] < x_index:
            lo = mid + 1
        else:
            hi = mid
    return count


def growth_table(ns=(10, 1000, 10**6)):          # exercise 13
    funcs = {"100 n": lambda n: 100 * n, "n * n": lambda n: n * n,
             "n * h(n)": lambda n: n * h(n), "h(n)": h, "1000": lambda n: 1000}
    return {name: [f(n) for n in ns] for name, f in funcs.items()}


def duplicates_by_sorting(t):                     # exercise 14: comparisons counted
    s = sorted(t)
    scans = max(len(s) - 1, 0)
    return any(s[k] == s[k + 1] for k in range(len(s) - 1)), scans


if __name__ == "__main__":
    print(double_loop(10), selection_count(10), h(1000))
    print(count_comparisons(sorted, [3, 1, 2]))
    print(max(binary_comparisons(1000, k) for k in range(-1, 1001)))
    print(growth_table())
