"""town_flow.py: buses an hour from the Bus Depot to the Football Ground."""
from maxflow import max_flow, min_cut
from town_net import PLACES, town_network

DEPOT, GROUND = 16, 15
net, roads = town_network()
log = []
value, flow = max_flow(net, DEPOT, GROUND, log=log)
print(f"{len(PLACES)} places, {len(net.cap)} directed road edges")
for path, delta in log:
    print(f"augment {delta:2} along {len(path) - 1:2} roads:", "-".join(map(str, path)))
print("maximum flow:", value, "buses an hour")
side, cut = min_cut(net, flow, DEPOT)
print(f"minimum cut, {sum(net.cap[e] for e in cut)} buses an hour:")
for u, v in cut:
    print(f"   road {roads[(u, v)]:2}, {PLACES[u]} > {PLACES[v]}: {net.cap[(u, v)]}")
