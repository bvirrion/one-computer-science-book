"""exo_inadmissible.py: A* with three times the straight-line distance."""
from state_space import astar
from town_map import PLACES, ROADS, straight

for s, t in [(2, 14), (30, 22), (16, 13)]:
    def goal(x, t=t):
        return x == t

    for k in (1, 3):
        path, cost, n = astar(s, goal, lambda x: ROADS.get(x, []),
                              lambda x, t=t, k=k: k * straight(x, t))
        print(f"{PLACES[s]} to {PLACES[t]}, h = {k} x straight line: {cost} m,"
              f" {n} expanded, route {'-'.join(map(str, path))}")
