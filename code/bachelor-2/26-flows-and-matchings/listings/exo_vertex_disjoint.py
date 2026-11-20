"""exo_vertex_disjoint.py: routes that share no place: each place is split into an
entrance and an exit joined by an edge of capacity 1."""
import csv

from maxflow import Network, max_flow
from town_net import PLACES, TOWN

net = Network()
for p in PLACES:
    net.add_edge(("in", p), ("out", p), 1)
with open(TOWN / "roads.csv", newline="") as f:
    for r in csv.DictReader(f):
        u, v = int(r["from_place"]), int(r["to_place"])
        net.add_edge(("out", u), ("in", v), 1)
        net.add_edge(("out", v), ("in", u), 1)
for s, t in [(2, 8), (16, 15), (30, 1)]:
    value, _ = max_flow(net, ("out", s), ("in", t))
    print(f"{PLACES[s]} to {PLACES[t]}: {value} routes with no place in common")
