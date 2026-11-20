"""selection.py: which library projects to run, when projects share equipment that
must be bought; a minimum cut, checked against all 32 choices."""
import itertools

from maxflow import Network, max_flow, min_cut

PROFIT = {"reading club": 9, "film nights": 7, "coding club": 8, "map room": 4,
          "story hour": 3}  # what each project brings, in hundreds a year
COST = {"projector": 6, "laptops": 10, "big table": 3, "screen": 4}
NEEDS = {"reading club": ["big table"], "film nights": ["projector", "screen"],
         "coding club": ["laptops", "projector"], "map room": ["big table", "screen"],
         "story hour": []}

net = Network()
for p, gain in PROFIT.items():
    net.add_edge("s", p, gain)
    for e in NEEDS[p]:
        net.add_edge(p, e, sum(PROFIT.values()) + 1)  # never cut
for e, cost in COST.items():
    net.add_edge(e, "t", cost)
cut_value, flow = max_flow(net, "s", "t")
side, _ = min_cut(net, flow, "s")
chosen = [p for p in PROFIT if p in side]
print(f"run: {', '.join(chosen)}; buy: {', '.join(e for e in COST if e in side)}")
print("profit", sum(PROFIT.values()) - cut_value, "= total profits",
      sum(PROFIT.values()), "- minimum cut", cut_value)


def gain(projects):
    equipment = {e for p in projects for e in NEEDS[p]}
    return sum(PROFIT[p] for p in projects) - sum(COST[e] for e in equipment)


best = max((c for k in range(6) for c in itertools.combinations(PROFIT, k)), key=gain)
print("best of all 32 choices:", gain(best), "with", ", ".join(best))
