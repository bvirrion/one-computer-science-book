"""segments.py: k segments of one length covering n points on a line: the smallest
length, by dichotomy on the answer."""

import csv
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def covers(xs, k, length):
    """Can k segments of this length cover the sorted points xs? (greedy)"""
    used, end = 0, None
    for x in xs:
        if end is None or x > end:  # x is not covered: a new segment starts at x
            used += 1
            end = x + length
    return used <= k


def smallest_length(xs, k):
    """The smallest integer length that works: covers is false below it, true above."""
    lo, hi = 0, xs[-1] - xs[0]  # covers(hi) is true: one segment suffices
    calls = 0
    while lo < hi:  # the answer is in [lo, hi]
        mid = (lo + hi) // 2
        calls += 1
        if covers(xs, k, mid):
            hi = mid
        else:
            lo = mid + 1
    return lo, calls


def main():
    with open(TOWN / "places.csv", newline="") as f:
        xs = sorted(int(r["x_m"]) for r in csv.DictReader(f))
    print(f"{len(xs)} places, x from {xs[0]} to {xs[-1]} m")
    print(f"{'k':>2} {'length (m)':>10} {'calls':>5}")
    for k in range(1, 9):
        length, calls = smallest_length(xs, k)
        print(f"{k:2} {length:10} {calls:5}")


if __name__ == "__main__":
    main()
