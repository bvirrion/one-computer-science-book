"""Distance-vector routing: every round, each router learns its neighbours' tables."""
from network import by_rate, graph


def dv_round(g, tables):
    """One round: each router rebuilds its table from its neighbours' tables."""
    new = {}
    for r in g:
        table = {r: (0, r)}
        for n, cost in g[r].items():
            for dest, (d, _) in tables[n].items():   # n says: I reach dest at d
                if dest not in table or cost + d < table[dest][0]:
                    table[dest] = (cost + d, n)       # better through n
        new[r] = table
    return new


def converge(g, tables, show=None):
    """Run rounds until no table changes; return the tables and the rounds."""
    rounds = 0
    while True:
        new = dv_round(g, tables)
        if new == tables:
            return tables, rounds
        tables, rounds = new, rounds + 1
        if show:
            t = new[show]
            row = "  ".join(f"{d}:{t[d][0]:>4}" if d in t else f"{d}:   -" for d in g)
            print(f"round {rounds:2}  {show} knows  {row}")


if __name__ == "__main__":
    g = graph(by_rate)
    start = {r: {r: (0, r)} for r in g}          # each router knows only itself
    tables, rounds = converge(g, start, show="A")
    print("stable after", rounds, "rounds; A's table (destination: cost, next hop):")
    print("  ".join(f"{d}: {c} {n}" for d, (c, n) in tables["A"].items() if d != "A"))
