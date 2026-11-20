"""Hop-count routing on a line A - B - C, where 16 means unreachable."""
INFINITY = 16


def dv_round(g, tables, split_horizon=False):
    new = {}
    for r in g:
        table = {r: (0, r)}
        for n, cost in g[r].items():
            for dest, (d, via) in tables[n].items():
                if split_horizon and via == r:
                    continue                     # n does not tell r a route through r
                d = min(cost + d, INFINITY)
                if dest not in table or d < table[dest][0]:
                    table[dest] = (d, n)
        new[r] = table
    return new


def after_failure(split_horizon):
    """Stable tables of the line; then B - C fails, and the distances to C change."""
    line = {"A": {"B": 1}, "B": {"A": 1, "C": 1}, "C": {"B": 1}}
    tables = {r: {r: (0, r)} for r in line}
    for _ in range(3):
        tables = dv_round(line, tables, split_horizon)
    print("before:  A", tables["A"]["C"][0], " B", tables["B"]["C"][0])
    cut = {"A": {"B": 1}, "B": {"A": 1}, "C": {}}
    rounds = 0
    while True:
        new = dv_round(cut, tables, split_horizon)
        a, b = (new[r].get("C", (INFINITY,))[0] for r in "AB")
        if new == tables:
            return rounds
        tables, rounds = new, rounds + 1
        print(f"round {rounds:2}: A {a:2}  B {b:2}")


if __name__ == "__main__":
    print("both A and B unreachable after", after_failure(False), "rounds")
