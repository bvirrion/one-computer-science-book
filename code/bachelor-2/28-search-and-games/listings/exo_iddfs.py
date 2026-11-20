"""exo_iddfs.py: iterative deepening against breadth-first search on the 8-puzzle:
states expanded, and states kept in memory at once."""
import random

from eight_puzzle import GOAL, scrambled, successors
from state_space import bfs, iterative_deepening

rng = random.Random(5)
for walk in [20, 40, 80]:
    start = scrambled(walk, rng)
    p1, n1 = bfs(start, lambda s: s == GOAL, successors)
    p2, n2 = iterative_deepening(start, lambda s: s == GOAL, successors)
    assert len(p1) == len(p2)
    print(f"depth {len(p1) - 1:2}: BFS expands {n1:5}, iterative deepening {n2:6};"
          f" IDDFS keeps a path of {len(p2)} states")
