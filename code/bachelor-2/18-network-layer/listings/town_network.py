"""town_network.py: a router at every place of the town, a link along every road."""
import csv
from pathlib import Path

from distance_vector import INF, converge, dv_round, link
from link_state import tables

TOWN = Path(__file__).resolve().parents[4] / "data" / "town"


def load(costs="length"):
    with open(TOWN / "places.csv", encoding="utf-8") as f:
        names = {r["place_id"]: r["name"] for r in csv.DictReader(f)}
    g = {}
    with open(TOWN / "roads.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):            # links work both ways, even on road 1
            cost = int(r["length_m"]) // 10 if costs == "length" else 1
            link(g, r["from_place"], r["to_place"], cost)
    return g, names


if __name__ == "__main__":
    g, names = load()
    dv, rounds = converge(g, inf=10**9)
    ls = tables(g)
    same = all(dv[u][d][0] == ls[u][0][d] for u in g for d in g)
    print(f"{len(g)} routers, {sum(map(len, g.values())) // 2} links")
    print(f"distance vector: {rounds} changing rounds; equals Dijkstra: {same}")

    hops, _ = load(costs="hops")
    dvh, rounds = converge(hops)
    lost = [p for p, n in names.items() if n.startswith("Lighthouse")][0]
    far = max(dvh[u][lost][0] for u in hops)
    print(f"hop counts: {rounds} rounds; farthest from {names[lost]}: {far} hops")
    for v in list(hops[lost]):                 # the router at that place breaks down
        del hops[v][lost]
    del hops[lost]
    dvh = {u: t for u, t in dvh.items() if u != lost}
    for r in range(1, 40):
        dvh = dv_round(hops, dvh)
        low = min(dvh[u][lost][0] for u in hops)
        high = max(dvh[u][lost][0] for u in hops)
        if r <= 3 or low == INF:
            print(f"round {r:2}: distances to it from {low} to {high}")
        if low == INF:
            break
    print(f"count to infinity: {r} rounds; link state: one recomputation per router")
