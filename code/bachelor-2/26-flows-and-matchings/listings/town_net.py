"""town_net.py: the town's roads as a flow network, in buses an hour."""
import csv
from pathlib import Path

from maxflow import Network

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def rows(name):
    with open(TOWN / f"{name}.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


PLACES = {int(p["place_id"]): p["name"] for p in rows("places")}


def buses_per_hour(speed_kmh):
    """The stated rule: a road takes (speed - 10) buses an hour in each direction."""
    return speed_kmh - 10


def town_network():
    net, roads = Network(), {}
    for r in rows("roads"):
        u, v = int(r["from_place"]), int(r["to_place"])
        c = buses_per_hour(int(r["speed_kmh"]))
        net.add_edge(u, v, c)
        roads[(u, v)] = int(r["road_id"])
        if r["one_way"] == "0":
            net.add_edge(v, u, c)
            roads[(v, u)] = int(r["road_id"])
    return net, roads
