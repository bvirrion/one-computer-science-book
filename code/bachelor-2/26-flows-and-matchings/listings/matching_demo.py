"""matching_demo.py: five readers, five reading slots; the matching grows path by
path."""
from matching import max_matching
from maxflow import Network, max_flow

ADJ = {"Ada": ["Mon", "Tue"], "Ben": ["Mon"], "Cy": ["Tue", "Wed", "Thu"],
       "Dee": ["Wed", "Fri"], "Eve": ["Mon", "Wed"]}
log = []
match = max_matching(ADJ, log)
for u, changed in log:
    print(f"{u:3}: new pairs", ", ".join(f"{w}-{v}" for v, w in changed.items()))
pairs = sorted((u, v) for v, u in match.items())
print("matching:", ", ".join(f"{u}-{v}" for u, v in pairs))

net = Network()  # the same question as a flow: s -> reader -> slot -> t, capacities 1
for u, slots in ADJ.items():
    net.add_edge("s", u, 1)
    for v in slots:
        net.add_edge(u, v, 1)
for v in sorted({v for slots in ADJ.values() for v in slots}):
    net.add_edge(v, "t", 1)
print("size", len(match), "= maximum flow", max_flow(net, "s", "t")[0])
