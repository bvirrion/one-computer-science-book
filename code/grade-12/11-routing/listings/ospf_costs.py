"""Link costs from link rates, and the route they choose against the hop count."""
from link_state import table
from network import RATES, REFERENCE, by_rate, graph, hops, route

for (u, v), rate in RATES.items():
    cost = by_rate(rate)
    print(f"{u} - {v}: {rate:>5} Mbit/s  cost {REFERENCE} // {rate:<5} = {cost:>4}")

for name, cost in [("hop count", hops), ("cost from rates", by_rate)]:
    g = graph(cost)
    tables = {r: table(g, r) for r in g}
    path = route(tables, "A", "E")
    rate = min(RATES.get((u, v)) or RATES[(v, u)] for u, v in zip(path, path[1:]))
    print(f"A to E by {name:15}: {' '.join(path):9} slowest link {rate} Mbit/s")
