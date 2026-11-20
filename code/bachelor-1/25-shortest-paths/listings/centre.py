"""centre.py: the eccentricity of each place (its greatest travel time to another
place), the centre of the town and its diameter."""

from floyd import floyd_warshall
from wgraph import names, roads


def eccentricities(order, d):
    return {v: max(d[i]) for i, v in enumerate(order)}


if __name__ == "__main__":
    name = names()
    order, d, _ = floyd_warshall(roads())
    ecc = eccentricities(order, d)
    ranked = sorted(ecc, key=lambda v: (ecc[v], v))
    for v in ranked[:3] + ranked[-2:]:
        far = order[d[order.index(v)].index(ecc[v])]
        print(f"{name[v]:16} {ecc[v]:4} s = {ecc[v] / 60:4.1f} min,"
              f" farthest {name[far]}")
    centre, edge = ranked[0], ranked[-1]
    print(f"centre: {name[centre]}, radius {ecc[centre]} s;"
          f" diameter {ecc[edge]} s = {ecc[edge] / 60:.1f} min")
