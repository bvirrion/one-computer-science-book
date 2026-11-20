"""disjoint_paths.py: routes between two places that share no road (Menger)."""
import csv

from maxflow import Network, max_flow, min_cut
from town_net import PLACES, TOWN


def paths_from_flow(flow, s, t):
    """Split a flow of unit edges into paths, following used edges from s."""
    left = {e for e, f in flow.items() if f > 0}
    paths = []
    while any(u == s for u, _ in left):
        path = [s]
        while path[-1] != t:
            edge = next(e for e in sorted(left) if e[0] == path[-1])
            left.remove(edge)
            path.append(edge[1])
        paths.append(path)
    return paths


net = Network()
with open(TOWN / "roads.csv", newline="") as f:
    for r in csv.DictReader(f):  # each road once, in either direction
        u, v = int(r["from_place"]), int(r["to_place"])
        net.add_edge(u, v, 1)
        net.add_edge(v, u, 1)
for s, t in [(2, 8), (16, 15), (30, 1)]:
    value, flow = max_flow(net, s, t)
    _, cut = min_cut(net, flow, s)
    print(f"{PLACES[s]} to {PLACES[t]}: {value} routes with no road in common;"
          f" a cut of {len(cut)} roads")
    for path in paths_from_flow(flow, s, t):
        print("   ", "-".join(map(str, path)))
