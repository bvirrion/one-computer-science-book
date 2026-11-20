"""subset_sum_dp.py: how many reading lists of exactly 1000 pages among the first n
books: a table over totals instead of a tree over subsets."""

import csv
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def pages(n):
    with open(TOWN / "books.csv", newline="") as f:
        return [int(row["pages"]) for row in csv.DictReader(f)][:n]


def count(values, target):
    """ways[t]: the number of subsets of the values seen so far with total t."""
    ways = [1] + [0] * target
    for v in values:
        for t in range(target, v - 1, -1):  # downwards: each value used at most once
            ways[t] += ways[t - v]
    return ways[target]


def main():
    for n in (16, 24, 40, 80):
        print(f"first {n:2} books: {count(pages(n), 1000):>12} lists of 1000 pages,"
              f" {n * 1001} cell updates at most")


if __name__ == "__main__":
    main()
