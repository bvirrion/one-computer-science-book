"""Whole objects only: the best value per kilogram first is no longer optimal."""
from itertools import combinations

OBJECTS = [("A", 6, 30), ("B", 5, 20), ("C", 5, 20)]   # name, kg, value
CAPACITY = 10

load, kg_used = [], 0
for name, kg, _ in sorted(OBJECTS, key=lambda o: o[2] / o[1], reverse=True):
    if kg_used + kg <= CAPACITY:
        load.append(name)
        kg_used += kg
print("greedy keeps", load, "value", sum(o[2] for o in OBJECTS if o[0] in load))

best = max((sum(o[2] for o in subset), [o[0] for o in subset])
           for r in range(len(OBJECTS) + 1)
           for subset in combinations(OBJECTS, r)
           if sum(o[1] for o in subset) <= CAPACITY)
print("every subset tried: best", best[1], "value", best[0])
