"""lis.py: the longest increasing subsequence, in O(n^2) by a table and in O(n log n)
by patience piles."""

import csv
from bisect import bisect_left
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def lis_table(a):
    """length[i]: the longest strictly increasing subsequence ending at a[i]."""
    length, before = [1] * len(a), [None] * len(a)
    for i in range(len(a)):
        for j in range(i):
            if a[j] < a[i] and length[j] + 1 > length[i]:
                length[i], before[i] = length[j] + 1, j
    if not a:
        return []
    i = max(range(len(a)), key=lambda k: length[k])
    out = []
    while i is not None:  # rebuild by following the predecessors
        out.append(a[i])
        i = before[i]
    return out[::-1]


def lis_patience(a):
    """The length: tops[k] is the smallest last key of an increasing subsequence of
    length k + 1 seen so far; each key goes on the leftmost pile whose top is >= it."""
    tops = []
    for x in a:
        k = bisect_left(tops, x)
        if k == len(tops):
            tops.append(x)  # a new pile on the right
        else:
            tops[k] = x
    return len(tops)


def main():
    a = [5, 2, 8, 6, 3, 6, 9, 7, 4, 10]
    print(a, "->", lis_table(a), "length", lis_patience(a))
    with open(TOWN / "books.csv", newline="") as f:
        years = [int(row["year"]) for row in csv.DictReader(f)]
    best = lis_table(years)
    print(f"years of the 80 books in catalogue order: longest increasing subsequence"
          f" {len(best)}, patience {lis_patience(years)}")
    print(" ", best)


if __name__ == "__main__":
    main()
