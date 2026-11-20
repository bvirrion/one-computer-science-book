"""exo_no_reverse.py: augmenting paths that only follow edges forwards."""
from maxflow import Network, max_flow, shortest_path


class Forward(Network):
    def residual(self, flow, u, v):  # unused capacity only: no cancelling
        return self.cap.get((u, v), 0) - flow.get((u, v), 0)


for cls in [Network, Forward]:
    net = cls()
    for u, v, c in [("s", "a", 8), ("s", "b", 6), ("a", "c", 7), ("a", "d", 5),
                    ("b", "c", 6), ("c", "t", 7), ("d", "t", 9)]:
        net.add_edge(u, v, c)
    log = []
    value, _ = max_flow(net, "s", "t", shortest_path, log)
    print(f"{cls.__name__:8} {value:3}:", ", ".join("".join(p) for p, _ in log))
