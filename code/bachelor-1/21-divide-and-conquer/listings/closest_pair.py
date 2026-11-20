"""closest_pair.py: the two closest points of a set in O(n log n), and brute force."""

import csv
import random
from math import dist, inf
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"
distances = 0  # distance computations since the last reset


def d(p, q):
    global distances
    distances += 1
    return dist(p, q)


def brute(points):
    return min(d(p, q) for i, p in enumerate(points) for q in points[i + 1:])


def closest(points):
    """The smallest distance between two of the points (at least two, all distinct)."""
    return solve(sorted(points))[0]


def solve(px):
    """(smallest distance, the points of px sorted by y); px is sorted by x."""
    n = len(px)
    if n <= 3:
        best = min((d(p, q) for i, p in enumerate(px) for q in px[i + 1:]), default=inf)
        return best, sorted(px, key=lambda p: p[1])
    mid = n // 2
    x_mid = px[mid][0]
    dl, left = solve(px[:mid])
    dr, right = solve(px[mid:])
    delta = min(dl, dr)
    py = merge_by_y(left, right)
    strip = [p for p in py if abs(p[0] - x_mid) < delta]  # still sorted by y
    for i, p in enumerate(strip):
        for q in strip[i + 1:i + 8]:  # at most 7 points can follow within delta
            if q[1] - p[1] >= delta:
                break
            delta = min(delta, d(p, q))
    return delta, py


def merge_by_y(a, b):
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i][1] <= b[j][1]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    return out + a[i:] + b[j:]


def places():
    with open(TOWN / "places.csv", newline="") as f:
        return {(int(r["x_m"]), int(r["y_m"])): r["name"] for r in csv.DictReader(f)}


def main():
    global distances
    town = places()
    delta = closest(list(town))
    p, q = [(p, q) for p in town for q in town if p < q and dist(p, q) == delta][0]
    print(f"town: {len(town)} places; closest: {town[p]} and {town[q]}, {delta:.0f} m")
    rng = random.Random(21)
    print(f"{'n':>5} {'divide and conquer':>18} {'brute force':>11}")
    for n in (250, 500, 1000, 2000):
        pts = list({(rng.random(), rng.random()) for _ in range(n)})
        distances = 0
        a = closest(pts)
        dc = distances
        distances = 0
        assert a == brute(pts)
        print(f"{n:5} {dc:18} {distances:11}")


if __name__ == "__main__":
    main()
