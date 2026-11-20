"""An invented network of seven routers, with the rate of each link in Mbit/s."""

RATES = {("A", "B"): 1000, ("A", "C"): 100, ("B", "C"): 1000, ("B", "D"): 100,
         ("C", "E"): 10, ("D", "E"): 1000, ("D", "F"): 1000, ("E", "G"): 100,
         ("F", "G"): 1000}
REFERENCE = 10_000                               # Mbit/s: a link this fast costs 1


def graph(cost, down=()):
    """Neighbours of each router with the cost of each link; links in down are cut."""
    g = {}
    for (u, v), rate in RATES.items():
        if (u, v) in down or (v, u) in down:
            continue
        g.setdefault(u, {})[v] = cost(rate)
        g.setdefault(v, {})[u] = cost(rate)
    return dict(sorted(g.items()))


def hops(rate):
    return 1                                     # every link counts the same


def by_rate(rate):
    return REFERENCE // rate                     # faster links cost less


def route(tables, source, target):
    """Follow the next hops from source; tables[r][dest] = (distance, next hop)."""
    path = [source]
    while path[-1] != target:
        path.append(tables[path[-1]][target][1])
    return path
