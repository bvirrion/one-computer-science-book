"""mst_town.py: the town's roads as an undirected weighted graph, by length."""

import csv
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def rows(name):
    with open(TOWN / f"{name}.csv", newline="") as f:
        return list(csv.DictReader(f))


def town():
    """(vertices, edges): edges are (metres, u, v), one per road, direction ignored."""
    vertices = [int(p["place_id"]) for p in rows("places")]
    edges = [(int(r["length_m"]), int(r["from_place"]), int(r["to_place"]))
             for r in rows("roads")]
    return vertices, edges


def names():
    return {int(p["place_id"]): p["name"] for p in rows("places")}


if __name__ == "__main__":
    vertices, edges = town()
    total = sum(w for w, _, _ in edges)
    print(f"{len(vertices)} places, {len(edges)} roads, {total} m of road in all")
