"""monotone.py: the monotone Boolean functions of n variables, counted by trying every
truth table: raising an input never lowers the output."""

from itertools import product


def monotone_count(n):
    rows = list(product((0, 1), repeat=n))
    count = 0
    for table in product((0, 1), repeat=len(rows)):
        f = dict(zip(rows, table))
        if all(f[x] <= f[y] for x in rows for y in rows
               if all(a <= b for a, b in zip(x, y))):
            count += 1
    return count
