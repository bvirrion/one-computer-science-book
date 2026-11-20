"""exo_maxflow.py: the network of exercise 3."""
from maxflow import Network, max_flow, min_cut

net = Network()
for u, v, c in [("s", "x", 9), ("s", "y", 7), ("x", "y", 3), ("x", "z", 4),
                ("y", "w", 6), ("z", "y", 2), ("z", "t", 5), ("w", "t", 7)]:
    net.add_edge(u, v, c)
log = []
value, flow = max_flow(net, "s", "t", log=log)
for path, delta in log:
    print(f"augment {delta} along {''.join(path)}")
side, cut = min_cut(net, flow, "s")
print(f"maximum flow {value}; cut {', '.join(u + v for u, v in cut)};",
      f"side {sorted(side)}")
