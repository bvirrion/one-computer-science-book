"""bad_example.py: Ford-Fulkerson with an unlucky choice of paths, against BFS."""
from maxflow import Network, max_flow, shortest_path


def simple_paths(net, flow, u, t, seen):
    if u == t:
        yield [t]
        return
    for v in net.adj.get(u, []):
        if v not in seen and net.residual(flow, u, v) > 0:
            for rest in simple_paths(net, flow, v, t, seen | {v}):
                yield [u] + rest


def narrowest_path(net, flow, s, t):
    """The augmenting path with the smallest bottleneck: the worst choice."""
    def bottleneck(p):
        return min(net.residual(flow, u, v) for u, v in zip(p, p[1:]))
    paths = list(simple_paths(net, flow, s, t, {s}))
    return min(paths, key=bottleneck) if paths else None


for C in [10, 100, 1000]:
    net = Network()
    for u, v, c in [("s", "a", C), ("s", "b", C), ("a", "t", C), ("b", "t", C),
                    ("a", "b", 1)]:
        net.add_edge(u, v, c)
    for name, find in [("narrowest", narrowest_path), ("shortest", shortest_path)]:
        log = []
        value, _ = max_flow(net, "s", "t", find, log)
        first = ", ".join("".join(p) for p, _ in log[:2])
        print(f"C = {C:4}, {name:9} paths: flow {value:4},",
              f"{len(log):4} augmentations, first {first}")
