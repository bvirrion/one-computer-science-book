"""kmeanspp.py: k-means++ seeding against uniform random seeding, 20 seeds each."""
import random

from dataset import blobs
from kmeans import d2, lloyd


def seed_pp(points, k, rng):
    """The first centre uniformly; each next one a point drawn with probability
    proportional to its squared distance to the nearest centre already chosen."""
    centres = [rng.choice(points)]
    while len(centres) < k:
        w = [min(d2(p, c) for c in centres) for p in points]
        centres.append(rng.choices(points, weights=w)[0])
    return centres


if __name__ == "__main__":
    pts = blobs()
    starts = [("uniform", lambda r: r.sample(pts, 5)),
              ("k-means++", lambda r: seed_pp(pts, 5, r))]
    runs = {name: [lloyd(pts, start(random.Random(s))) for s in range(20)]
            for name, start in starts}
    best = min(r[2][-1] for rs in runs.values() for r in rs)
    for name, rs in runs.items():
        finals = [costs[-1] for _, _, costs in rs]
        steps = sum(len(costs) for _, _, costs in rs) / len(rs)
        hits = sum(c < best + 1e-9 for c in finals)
        print(f"{name:9}: best clustering {hits:2} times of 20, mean final cost"
              f" {sum(finals) / 20:6.1f}, worst {max(finals):6.1f}, {steps:.1f} steps")
