"""exo_manhattan.py: every solvable 8-puzzle state, its true distance to the goal by
breadth-first search backwards, against the two heuristics."""
from collections import Counter, deque

from eight_puzzle import GOAL, manhattan, misplaced, successors

dist, queue = {GOAL: 0}, deque([GOAL])
while queue:
    s = queue.popleft()
    for t, _ in successors(s):  # moves are reversible: same graph backwards
        if t not in dist:
            dist[t] = dist[s] + 1
            queue.append(t)
print(f"{len(dist)} states reachable; largest distance {max(dist.values())}")
for h in (misplaced, manhattan):
    over = sum(h(s) > d for s, d in dist.items())
    exact = sum(h(s) == d for s, d in dist.items())
    gap = Counter(d - h(s) for s, d in dist.items())
    print(f"{h.__name__:9}: above the true distance {over} times, equal {exact} times;"
          f" mean gap {sum(k * c for k, c in gap.items()) / len(dist):.2f}")
