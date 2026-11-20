"""karger_demo.py: two groups of four, all friends within a group, joined by two
friendships: one run traced, then the success rate over 10,000 runs."""
import itertools
import random

from karger import contract

V = list("abcdefgh")
E = (list(itertools.combinations("abcd", 2)) + list(itertools.combinations("efgh", 2))
     + [("d", "e"), ("c", "f")])
rng = random.Random(10)
log = []
cut, side = contract(V, E, rng, log)
print("contracted:", " ".join(u + v for u, v in log))
print(f"cut of {len(cut)} edges:", " ".join(u + v for u, v in cut),
      "| one side:", "".join(sorted(side)))
n, wins = len(V), 0
for _ in range(10_000):
    cut, _ = contract(V, E, rng)
    wins += len(cut) == 2
print(f"minimum cut found in {wins} of 10,000 runs;",
      f"bound 2/(n(n-1)) = {2 / (n * (n - 1)):.4f}")
