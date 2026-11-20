"""meet_middle.py: reading lists of exactly 1000 pages from the first n books, by
splitting the books in two halves: 2^(n/2) sums per half instead of 2^n subsets."""

import csv
from collections import Counter
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def pages(n):
    with open(TOWN / "books.csv", newline="") as f:
        return [int(row["pages"]) for row in csv.DictReader(f)][:n]


def all_sums(values):
    """The sums of the 2^len(values) subsets (with repetitions)."""
    sums = [0]
    for v in values:
        sums += [s + v for s in sums]  # each subset without v, then with v
    return sums


def count(values, target):
    """(number of subsets summing to target, sums computed)."""
    half = len(values) // 2
    left, right = all_sums(values[:half]), all_sums(values[half:])
    right_count = Counter(right)  # how many right subsets give each sum
    found = sum(right_count[target - s] for s in left)
    return found, len(left) + len(right)


def main():
    print(f"{'n':>2} {'lists':>8} {'subsets 2^n':>16} {'sums computed':>13}")
    for n in (16, 24, 32, 40):
        found, work = count(pages(n), 1000)
        print(f"{n:2} {found:8} {2**n:16} {work:13}")


if __name__ == "__main__":
    main()
