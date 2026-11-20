"""exo_mincut.py: the minimum cut read from the flow f3 of exercise 1."""
from maxflow import Network, min_cut

net = Network()
for u, v, c in [("s", "a", 8), ("s", "b", 6), ("a", "c", 7), ("a", "d", 5),
                ("b", "c", 6), ("c", "t", 7), ("d", "t", 9)]:
    net.add_edge(u, v, c)
f3 = {("s", "a"): 6, ("s", "b"): 6, ("a", "c"): 1, ("a", "d"): 5, ("b", "c"): 6,
      ("c", "t"): 7, ("d", "t"): 5}
for u, v in [("s", "a"), ("a", "c"), ("c", "b"), ("b", "s"), ("a", "d"), ("d", "t")]:
    print(f"residual {u}->{v}: {net.residual(f3, u, v)}")
side, cut = min_cut(net, f3, "s")
print(f"reachable: {sorted(side)}; cut {', '.join(u + v for u, v in cut)}")
