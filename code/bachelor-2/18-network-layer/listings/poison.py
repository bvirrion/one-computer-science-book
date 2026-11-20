"""poison.py: poisoned reverse on two and on three routers (ex. 10)."""
from distance_vector import INF, converge, dv_round, link


def after_failure(edges, a, b, dest, poison):
    g = {}
    for x, y in edges:
        link(g, x, y, 1)
    tables, _ = converge(g, poison=poison)
    del g[a][b], g[b][a]
    for r in range(1, 40):
        tables = dv_round(g, tables, poison=poison)
        if all(tables[u][dest][0] == INF for u in g if u != dest):
            return r
    return None


line = [("A", "B"), ("B", "C")]
loop = [("A", "B"), ("B", "C"), ("A", "C"), ("C", "D")]
cases = [("line A-B-C, B-C fails", line, "B", "C", "C"),
         ("triangle A-B-C plus D, C-D fails", loop, "C", "D", "D")]
for name, edges, a, b, dest in cases:
    for poison in (False, True):
        r = after_failure(edges, a, b, dest, poison)
        how = "poisoned reverse" if poison else "plain"
        print(f"{name:34} {how:17} every router at {INF} after {r} rounds")
