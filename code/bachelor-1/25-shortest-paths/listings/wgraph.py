"""wgraph.py: the town's roads as a weighted directed graph, in metres or in seconds."""

import csv
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def rows(name):
    with open(TOWN / f"{name}.csv", newline="") as f:
        return list(csv.DictReader(f))


def roads(weight="seconds"):
    """adj[u] is a list of (v, w); a one-way road gives one arc, any other road two.
    The time of a road is its length at its speed limit, rounded to the second."""
    adj = {int(p["place_id"]): [] for p in rows("places")}
    for r in rows("roads"):
        a, b = int(r["from_place"]), int(r["to_place"])
        metres, kmh = int(r["length_m"]), int(r["speed_kmh"])
        w = metres if weight == "metres" else round(metres * 3.6 / kmh)
        adj[a].append((b, w))
        if r["one_way"] == "0":
            adj[b].append((a, w))
    return adj


def names():
    return {int(p["place_id"]): p["name"] for p in rows("places")}


if __name__ == "__main__":
    adj = roads()
    speeds = sorted({int(r["speed_kmh"]) for r in rows("roads")})
    arcs = sum(map(len, adj.values()))
    print(f"{len(adj)} places, {arcs} arcs, speed limits {speeds} km/h")
    print("from the Station:", [(names()[v], w) for v, w in adj[2]])
