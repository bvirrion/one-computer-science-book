"""exo_bfs_order.py: the order in which breadth-first search expands the town's places
from the Bus Depot, neighbours taken in the order of the road table."""
from collections import deque

from town_map import ROADS

order, depth, queue = [], {16: 0}, deque([16])
while queue:
    u = queue.popleft()
    order.append(u)
    for v, _ in ROADS.get(u, []):
        if v not in depth:
            depth[v] = depth[u] + 1
            queue.append(v)
for d in range(max(depth.values()) + 1):
    print(f"depth {d}:", [p for p in order if depth[p] == d])
