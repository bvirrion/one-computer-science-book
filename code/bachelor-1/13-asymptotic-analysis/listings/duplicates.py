"""duplicates.py: three ways to find the books borrowed more than once
among the first n loans of the town's library, each counting its operations."""

import csv
from pathlib import Path

from sorts import merge_sort

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"
with open(TOWN / "loans.csv", newline="") as f:
    BOOKS = [int(row["book_id"]) for row in csv.DictReader(f)]


def by_pairs(xs):
    ops, found = 0, set()
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            ops += 1  # one comparison
            if xs[i] == xs[j]:
                found.add(xs[i])
    return found, ops


def by_sorting(xs):
    counter = [0]
    s = merge_sort(xs, counter)
    found = set()
    for i in range(1, len(s)):
        counter[0] += 1  # one comparison of neighbours
        if s[i] == s[i - 1]:
            found.add(s[i])
    return found, counter[0]


def by_set(xs):
    ops, seen, found = 0, set(), set()
    for x in xs:
        ops += 1  # one look-up in seen, with its insertion
        if x in seen:
            found.add(x)
        seen.add(x)
    return found, ops


if __name__ == "__main__":
    print(f"{'n':>3} {'dup':>3} {'pairs':>6} {'sorting':>7} {'set':>3}   ratios")
    previous = None
    for n in [25, 50, 100, 200, 400]:
        results = [method(BOOKS[:n]) for method in (by_pairs, by_sorting, by_set)]
        assert results[0][0] == results[1][0] == results[2][0]
        ops = [r[1] for r in results]
        ratios = "" if previous is None else " ".join(
            f"{o / p:4.2f}" for o, p in zip(ops, previous))
        print(f"{n:3d} {len(results[0][0]):3d} {ops[0]:6d} {ops[1]:7d} {ops[2]:3d}"
              f"   {ratios}".rstrip())
        previous = ops
