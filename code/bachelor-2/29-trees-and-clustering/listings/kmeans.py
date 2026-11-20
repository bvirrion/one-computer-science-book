"""kmeans.py: Lloyd's algorithm on the planted points, then the same from 20 random
starts: different starts stop at different local minima."""
import random

from dataset import blobs


def d2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def assign(points, centres):
    """The index of the nearest centre of each point (the first one on a tie)."""
    return [min(range(len(centres)), key=lambda j: d2(p, centres[j])) for p in points]


def cost(points, centres, a):
    return sum(d2(p, centres[j]) for p, j in zip(points, a))


def lloyd(points, centres):
    """Alternate the two steps until the assignment no longer changes; return the
    centres, the assignment and the cost after each assignment step."""
    a, costs = None, []
    while True:
        new = assign(points, centres)
        costs.append(cost(points, centres, new))
        if new == a:
            return centres, a, costs
        a = new
        centres = [centroid([p for p, j in zip(points, a) if j == i]) or centres[i]
                   for i in range(len(centres))]  # an empty cluster keeps its centre


def centroid(group):
    if not group:
        return None
    n = len(group)
    return (sum(p[0] for p in group) / n, sum(p[1] for p in group) / n)


if __name__ == "__main__":
    pts = blobs()
    _, _, costs = lloyd(pts, random.Random(3).sample(pts, 5))
    print("seed 3, cost after each step:", " ".join(f"{c:.1f}" for c in costs))
    finals = sorted(lloyd(pts, random.Random(s).sample(pts, 5))[2][-1]
                    for s in range(20))
    best = [c for c in finals if c < finals[0] + 1e-9]
    print(f"20 random starts: {len(best)} stop at cost {finals[0]:.1f}, the others at")
    print("   ", " ".join(f"{c:.1f}" for c in finals[len(best):]))
