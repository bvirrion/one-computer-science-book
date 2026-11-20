"""exo_kmeanspp.py: uniform and k-means++ seeding over 100 seeds each."""
import random
from collections import Counter

from dataset import blobs
from kmeans import lloyd
from kmeanspp import seed_pp

pts = blobs()
for name, start in [("uniform", lambda r: r.sample(pts, 5)),
                    ("k-means++", lambda r: seed_pp(pts, 5, r))]:
    finals = Counter(round(lloyd(pts, start(random.Random(s)))[2][-1])
                     for s in range(100))
    top = ", ".join(f"{c} in {n}" for c, n in sorted(finals.items())[:3])
    print(f"{name:9}: {len(finals)} different final costs; runs ending at {top}, ...")
