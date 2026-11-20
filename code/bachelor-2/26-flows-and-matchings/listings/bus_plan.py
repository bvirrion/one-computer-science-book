"""bus_plan.py: the stadium bus plan. The flow from the Bus Depot to the Football
Ground, the roads of the minimum cut, what widening each one buys, and the drivers."""
from matching import max_matching
from maxflow import max_flow, min_cut
from town_net import PLACES, town_network

DEPOT, GROUND = 16, 15


def plan(widen=None, by=20):
    net, roads = town_network()
    if widen is not None:  # one road made wider, in the direction the cut uses
        net.cap[widen] += by
    value, flow = max_flow(net, DEPOT, GROUND)
    side, cut = min_cut(net, flow, DEPOT)
    return value, cut, net, roads


value, cut, net, roads = plan()
print(f"maximum flow {value} buses an hour = capacity of the minimum cut:")
for e in cut:
    print(f"   road {roads[e]:2}, {PLACES[e[0]]} > {PLACES[e[1]]}: {net.cap[e]}")
for e in cut:
    print(f"widen road {roads[e]:2} by 20: {plan(e)[0]} buses an hour")
value, flow = max_flow(net, DEPOT, GROUND)
near = {GROUND}  # the places that can still reach the ground in the residual network
while grown := {u for u in net.adj for v in near
                if u not in near and net.residual(flow, u, v) > 0}:
    near |= grown
far = sorted((roads[e], c) for e, c in net.cap.items()
             if e[0] not in near and e[1] in near and c > 0)
print("cut nearest the ground: roads", ", ".join(f"{r} ({c})" for r, c in far))

# Part IV: each bus needs a driver with the right licence; one bus each.
BUSES = {f"B{i}": ["single", "double", "electric"][i % 3] for i in range(1, 10)}
DRIVERS = {"Ana": {"single"}, "Bo": {"single", "double"}, "Cal": {"electric"},
           "Dia": {"double"}, "Eli": {"single", "electric"}, "Fen": {"double"},
           "Gus": {"single"}, "Hal": {"electric", "double"}, "Ivo": {"single"}}
adj = {d: [b for b, kind in BUSES.items() if kind in lic] for d, lic in DRIVERS.items()}
for ill in [None, "Hal"]:
    match = max_matching({d: bs for d, bs in adj.items() if d != ill})
    print(f"{ill or 'nobody'} ill, {len(match)} of {len(BUSES)} driven:",
          " ".join(f"{b}-{d}" for b, d in sorted(match.items())))
