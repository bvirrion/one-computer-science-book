"""friends_problem.py: Karger's algorithm on the town's friendship network."""
import random
from collections import Counter

from karger import contract
from town import friendships


def group_of(v, edges):
    group, todo = {v}, [v]
    while todo:
        u = todo.pop()
        for a, b in edges:
            for x, y in [(a, b), (b, a)]:
                if x == u and y not in group:
                    group.add(y)
                    todo.append(y)
    return group


def core(vertices, edges):
    """Set aside, again and again, the people with fewer than two friends left."""
    vs = set(vertices)
    while low := {v for v in vs if sum(v in e and set(e) <= vs for e in edges) < 2}:
        vs -= low
    return sorted(vs), [e for e in edges if set(e) <= vs]


def measure(name, vertices, edges, rng, runs=10_000):
    sizes, cuts = Counter(), Counter()
    for _ in range(runs):
        cut, side = contract(vertices, edges, rng)
        sizes[len(cut)] += 1
        small = min(side, set(vertices) - side, key=lambda s: (len(s), sorted(s)))
        cuts[(len(cut), tuple(sorted(small)))] += 1
    best = min(sizes)
    n = len(vertices)
    print(f"{name}: {n} people, {len(edges)} friendships; smallest cut {best},"
          f" found in {sizes[best]:,} of {runs:,} runs")
    found = sorted((-c, s) for (k, s), c in cuts.items() if k == best)
    print(f"   bound 2/(n(n-1)) = {2 / (n * (n - 1)):.4f};"
          f" {len(found)} different minimum cuts found, the most frequent:")
    for c, s in found[:3]:
        print(f"      one side {list(s)}: {-c} runs")
    return cuts


E = friendships()
people = sorted({x for e in E for x in e})
big = sorted(group_of(1, E))
print(f"{len(people)} people have friends, {len(E)} friendships; two groups of"
      f" {len(big)} and {len(people) - len(big)} with no friendship between")
small = [e for e in E if e[0] not in big]
print("the smaller group's friendships:", " ".join(f"{a}-{b}" for a, b in small))
rng = random.Random(9)
measure("the larger group", big, [e for e in E if e[0] in big], rng)
cv, ce = core(big, [e for e in E if e[0] in big])
cuts = measure("its core", cv, ce, rng)
split = (2, (28, 29, 30, 32, 34, 36, 37, 38, 39))
print(f"   the cut that sets apart the 9 people {list(split[1])}: {cuts[split]} runs")
