"""subset_sum.py: reading lists of exactly 1000 pages from the library's first n books:
the include/exclude tree, with and without pruning."""

import csv
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def pages(n):
    with open(TOWN / "books.csv", newline="") as f:
        return [int(row["pages"]) for row in csv.DictReader(f)][:n]


def count(values, target, prune):
    """(solutions, nodes) of the include/exclude tree over values."""
    if prune:
        values = sorted(values, reverse=True)  # large first: overshoot early
    rest = [sum(values[i:]) for i in range(len(values) + 1)]  # undecided values
    stats = [0, 0]

    def visit(i, total):
        stats[1] += 1
        if prune and (total > target or total + rest[i] < target):
            return  # too much already, or even all the rest cannot reach the target
        if i == len(values):
            stats[0] += total == target
            return
        visit(i + 1, total + values[i])
        visit(i + 1, total)

    visit(0, 0)
    return stats[0], stats[1]


def main():
    print(f"{'n':>2} {'lists':>6} {'nodes, all':>11} {'nodes, pruned':>14}")
    for n in (12, 16, 20, 24):
        sols, pruned = count(pages(n), 1000, prune=True)
        full = 2 ** (n + 1) - 1  # without pruning, every node of the tree is visited
        print(f"{n:2} {sols:6} {full:11} {pruned:14}")


if __name__ == "__main__":
    main()
