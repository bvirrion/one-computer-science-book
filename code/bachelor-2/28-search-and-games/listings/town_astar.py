"""town_astar.py: shortest routes on the town map, by uniform-cost search (Dijkstra)
and by A* with the straight-line distance to the goal."""
from state_space import astar
from town_map import PLACES, ROADS, straight

shorter = [(u, v) for u in ROADS for v, d in ROADS[u] if d < straight(u, v)]
print(f"{len(PLACES)} places; roads shorter than the straight line: {len(shorter)}")
for s, t in [(16, 15), (30, 22), (2, 14)]:
    def goal(x, t=t):
        return x == t

    def h(x, t=t):
        return straight(x, t)

    path, d0, n0 = astar(s, goal, lambda x: ROADS.get(x, []))
    path1, d1, n1 = astar(s, goal, lambda x: ROADS.get(x, []), h)
    assert d0 == d1
    print(f"{PLACES[s]} to {PLACES[t]}: {d0} m, straight line {straight(s, t):.0f} m;"
          f" expanded {n0} (Dijkstra) and {n1} (A*)")
    print("   route:", "-".join(map(str, path1)))
