"""The link D - F fails: both methods find the new route from A to G."""
from dv_rounds import converge
from link_state import table
from network import by_rate, graph, route

g = graph(by_rate)
start = {r: {r: (0, r)} for r in g}
dv, _ = converge(g, start)                      # stable tables before the failure
print("before:     ", " ".join(route(dv, "A", "G")), " cost", dv["A"]["G"][0])

cut = graph(by_rate, down=[("D", "F")])
dv, rounds = converge(cut, dv, show="A")
print("distance vector:", rounds, "rounds;", " ".join(route(dv, "A", "G")),
      " cost", dv["A"]["G"][0])

ls = {r: table(cut, r) for r in cut}            # after flooding the change
print("link state:     ", " ".join(route(ls, "A", "G")), " cost", ls["A"]["G"][0])
