"""exo_karger_rep.py: Karger repeated r times on the graph of karger_demo.py; how often
the best of the r runs is the minimum cut, over 2,000 trials."""
import itertools
import random

from karger import karger

V = list("abcdefgh")
E = (list(itertools.combinations("abcd", 2)) + list(itertools.combinations("efgh", 2))
     + [("d", "e"), ("c", "f")])
rng = random.Random(13)
p, q = 0.2147, 2 / (8 * 7)  # measured in karger_demo.py; the bound
print("  r  success  1-(1-p)^r  1-(1-2/(n(n-1)))^r")
for r in [1, 2, 5, 10, 20]:
    wins = sum(len(karger(V, E, r, rng)[0]) == 2 for _ in range(2000)) / 2000
    print(f"{r:3}  {wins:7.3f}  {1 - (1 - p) ** r:9.3f}  {1 - (1 - q) ** r:18.3f}")
