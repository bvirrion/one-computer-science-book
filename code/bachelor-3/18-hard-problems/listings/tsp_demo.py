"""tsp_demo.py -- the delivery van: 12 of the town's places, the exact tour against tree
doubling and 2-opt; then 200 seeded choices of 12 places out of 30."""
import random

from tsp import held_karp, length, town_places, tree_doubling, two_opt

places = town_places()
van = places[:12]
best = length(van, held_karp(van))
doubled = tree_doubling(van)
print(f"12 places: optimum {best:,.0f} m")
print(f"  tree doubling {length(van, doubled):,.0f} m "
      f"(ratio {length(van, doubled) / best:.3f})")
print(f"  then 2-opt    {length(van, two_opt(van, doubled)):,.0f} m "
      f"(ratio {length(van, two_opt(van, doubled)) / best:.3f})")

rng, doubling, opt2 = random.Random(18), [], []
for _ in range(200):
    pts = rng.sample(places, 12)
    best = length(pts, held_karp(pts))
    tour = tree_doubling(pts)
    doubling.append(length(pts, tour) / best)
    opt2.append(length(pts, two_opt(pts, tour)) / best)
for name, r in (("tree doubling", doubling), ("then 2-opt", opt2)):
    print(f"200 instances, {name:<13}: mean ratio {sum(r) / len(r):.3f}, "
          f"worst {max(r):.3f}, optimal in {sum(x < 1 + 1e-9 for x in r)}")
