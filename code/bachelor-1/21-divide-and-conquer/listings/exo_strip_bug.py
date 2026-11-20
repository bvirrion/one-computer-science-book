"""exo_strip_bug.py: exercise 5, a strip that compares each point with the next only."""

import random
from math import dist


def closest(px):  # px sorted by x
    if len(px) <= 3:
        return min(dist(p, q) for i, p in enumerate(px) for q in px[i + 1:])
    mid = len(px) // 2
    delta = min(closest(px[:mid]), closest(px[mid:]))
    strip = [p for p in px if abs(p[0] - px[mid][0]) < delta]
    strip.sort(key=lambda p: p[1])
    for p, q in zip(strip, strip[1:]):  # only neighbours in the y order
        delta = min(delta, dist(p, q))
    return delta


if __name__ == "__main__":
    rng = random.Random(5)
    for trial in range(1, 10000):
        pts = sorted({(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(6)})
        true = min(dist(p, q) for i, p in enumerate(pts) for q in pts[i + 1:])
        if closest(pts) != true:
            print(f"trial {trial}: {pts}")
            print(f"returned {closest(pts):.3f}, true {true:.3f}")
            break
