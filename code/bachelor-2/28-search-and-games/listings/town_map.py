"""town_map.py: the town's places with their coordinates and its roads with their
lengths, as a weighted graph."""
import csv
import math
from pathlib import Path

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def rows(name):
    with open(TOWN / f"{name}.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


PLACES = {int(p["place_id"]): p["name"] for p in rows("places")}
XY = {int(p["place_id"]): (int(p["x_m"]), int(p["y_m"])) for p in rows("places")}
ROADS = {}  # place -> [(neighbour, length in metres)]
for r in rows("roads"):
    u, v, d = int(r["from_place"]), int(r["to_place"]), int(r["length_m"])
    ROADS.setdefault(u, []).append((v, d))
    if r["one_way"] == "0":
        ROADS.setdefault(v, []).append((u, d))


def straight(u, v):
    """The straight-line distance in metres: no road between u and v is shorter."""
    return math.dist(XY[u], XY[v])
