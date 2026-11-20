"""Exercises of the chapter on dynamic programming."""


def binomial(n, k, memo=None):                     # exercise 5
    if memo is None:
        memo = {}
    if k == 0 or k == n:
        return 1
    if (n, k) not in memo:
        memo[(n, k)] = binomial(n - 1, k - 1, memo) + binomial(n - 1, k, memo)
    return memo[(n, k)]


def binomial_bad(n, k, memo=None):                 # exercise 6: the staged fault
    if memo is None:
        memo = {}
    if k == 0 or k == n:
        return 1
    if n not in memo:                              # the key forgets k
        memo[n] = binomial_bad(n - 1, k - 1, memo) + binomial_bad(n - 1, k, memo)
    return memo[n]


def min_coins(amount, coins, memo=None):           # exercise 7, top-down
    if memo is None:
        memo = {}
    if amount == 0:
        return 0
    if amount not in memo:
        options = [min_coins(amount - c, coins, memo) for c in coins if c <= amount]
        options = [x for x in options if x is not None]
        memo[amount] = min(options) + 1 if options else None
    return memo[amount]


def lcs_wrong_order(a, b):                         # exercise 8: the staged fault
    n, m = len(a), len(b)
    t = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n, 0, -1):                      # from the end: t[i - 1] not ready
        for j in range(m, 0, -1):
            if a[i - 1] == b[j - 1]:
                t[i][j] = t[i - 1][j - 1] + 1
            else:
                t[i][j] = max(t[i - 1][j], t[i][j - 1])
    return t[n][m]


def grid_paths(rows, cols):                        # exercise 9
    p = [[1] * (cols + 1) for _ in range(rows + 1)]
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            p[r][c] = p[r - 1][c] + p[r][c - 1]
    return p[rows][cols]


def diff_lines(old, new):                          # exercise 10
    from lcs import lcs_table
    t = lcs_table(old, new)
    i, j, out = len(old), len(new), []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and old[i - 1] == new[j - 1]:
            out.append("  " + old[i - 1])
            i, j = i - 1, j - 1
        elif j > 0 and (i == 0 or t[i][j - 1] >= t[i - 1][j]):
            out.append("+ " + new[j - 1])
            j -= 1
        else:
            out.append("- " + old[i - 1])
            i -= 1
    return out[::-1]


def edit_operations(a, b):                         # exercise 13
    from align import alignment, distance_table
    ops = []
    for x, y in alignment(a, b, distance_table(a, b)):
        if x is None:
            ops.append(f"insert {y}")
        elif y is None:
            ops.append(f"delete {x}")
        elif x != y:
            ops.append(f"replace {x} by {y}")
    return ops


def longest_increasing(t):                         # exercise 15
    if not t:
        return []
    best = [1] * len(t)                            # best[i]: longest ending at t[i]
    before = [None] * len(t)
    for i in range(len(t)):
        for j in range(i):
            if t[j] < t[i] and best[j] + 1 > best[i]:
                best[i], before[i] = best[j] + 1, j
    i = max(range(len(t)), key=lambda k: best[k])
    out = []
    while i is not None:
        out.append(t[i])
        i = before[i]
    return out[::-1]


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
    print(binomial(10, 5), binomial_bad(10, 5), min_coins(7, [1, 3, 4]))
    print(lcs_wrong_order("LIBRARY", "LITERARY"), grid_paths(5, 5))
    print(edit_operations("kitten", "sitting"))
    print(longest_increasing([5, 2, 8, 6, 3, 6, 9, 7]))
    print(diff_lines(["a", "b", "c", "d"], ["a", "c", "d", "e"]))
