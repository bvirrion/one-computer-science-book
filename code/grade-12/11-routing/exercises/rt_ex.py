"""Exercises of the chapter on routing."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from count_to_infinity import INFINITY  # noqa: E402
from dv_rounds import converge, dv_round  # noqa: E402
from link_state import flood, table  # noqa: E402
from network import by_rate, graph, hops, route  # noqa: E402


def dv_update(table_, neighbour, neighbour_table, cost):      # exercise 5
    """The router's table after hearing one neighbour; tables map dest -> (d, via)."""
    new = dict(table_)
    for dest, (d, _) in neighbour_table.items():
        if dest not in new or cost + d < new[dest][0]:
            new[dest] = (cost + d, neighbour)
    return new


def dv_round_larger(g, tables):                               # exercise 6: the fault
    new = {}
    for r in g:
        t = {r: (0, r)}
        for n, cost in g[r].items():
            for dest, (d, _) in tables[n].items():
                if dest not in t or cost + d > t[dest][0]:
                    t[dest] = (cost + d, n)
        new[r] = t
    return new


def line(n):
    names = [f"R{k}" for k in range(1, n + 1)]
    g = {r: {} for r in names}
    for a, b in zip(names, names[1:]):
        g[a][b] = g[b][a] = 1
    return g


def ring(n):
    g = line(n)
    g["R1"][f"R{n}"] = g[f"R{n}"]["R1"] = 1
    return g


def cost_from_rate(rate, ref):                                # exercise 8
    return max(1, ref // rate)


def rounds_from_scratch(g):                                   # exercise 7
    return converge(g, {r: {r: (0, r)} for r in g})[1]


def flood_messages(g):                                        # exercise 11
    return flood(g)[1]


def count_rounds(g, cut, dest, poison=False):                 # exercises 13 and 14
    """Stable tables of g, then the network cut: rounds until nothing changes."""
    tables = converge(g, {r: {r: (0, r)} for r in g})[0]
    rounds = 0
    while True:
        new = {}
        for r in cut:
            t = {r: (0, r)}
            for n, cost in cut[r].items():
                for d_, (d, via) in tables[n].items():
                    if poison and via == r:
                        d = INFINITY                  # poisoned reverse
                    d = min(cost + d, INFINITY)
                    if d_ not in t or d < t[d_][0]:
                        t[d_] = (d, n)
            new[r] = t
        if new == tables:
            return rounds, {r: tables[r].get(dest, (INFINITY,))[0] for r in cut}
        tables, rounds = new, rounds + 1


def routes():                                                 # exercises 2, 3, 9
    out = {}
    for name, cost, down in [("hops", hops, ()), ("cost", by_rate, ()),
                             ("cut B-D", by_rate, [("B", "D")])]:
        g = graph(cost, down)
        tables = {r: table(g, r) for r in g}
        out[name] = (route(tables, "A", "G"), tables["A"]["G"][0])
    return out


if __name__ == "__main__":
    g = graph(by_rate)
    t1 = dv_round(g, {r: {r: (0, r)} for r in g})
    print("ex1 D:", t1["D"])
    print(routes())
    print("E table:", table(g, "E"))
    t = {r: {r: (0, r)} for r in g}
    for k in range(6):
        t = dv_round_larger(g, t)
        print("ex6", k + 1, t["A"].get("E"))
    print("ex7", [rounds_from_scratch(line(n)) for n in range(2, 8)])
    print("ex11", [(n, flood_messages(ring(n))) for n in range(3, 9)])
    four = line(4)
    cut4 = line(4)
    del cut4["R3"]["R4"], cut4["R4"]["R3"]
    print("ex13", count_rounds(four, cut4, "R4"))
    three = line(3)
    cut3 = line(3)
    del cut3["R2"]["R3"], cut3["R3"]["R2"]
    print("ex14", count_rounds(three, cut3, "R3"))
    print("ex14", count_rounds(three, cut3, "R3", True))
    print("ex13b", count_rounds(four, cut4, "R4", True))
