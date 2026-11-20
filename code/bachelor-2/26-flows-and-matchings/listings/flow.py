"""flow.py: Edmonds-Karp on a small network, path by path, and the minimum cut."""
from maxflow import Network, max_flow, min_cut

EDGES = [("s", "a", 8), ("s", "b", 6), ("a", "c", 7), ("a", "d", 5), ("b", "c", 6),
         ("c", "t", 7), ("d", "t", 9)]
net = Network()
for u, v, c in EDGES:
    net.add_edge(u, v, c)
log = []
value, flow = max_flow(net, "s", "t", log=log)
for path, delta in log:
    print(f"augment {delta:2} along {' -> '.join(path)}")
print("maximum flow", value)
print("flow/capacity:", ", ".join(f"{u}{v} {flow.get((u, v), 0)}/{c}"
                                  for u, v, c in EDGES))
side, cut = min_cut(net, flow, "s")
capacity = sum(net.cap[e] for e in cut)
print(f"reachable from s in the residual network: {sorted(side)}")
print(f"minimum cut: {', '.join(u + v for u, v in cut)}, capacity {capacity}")
