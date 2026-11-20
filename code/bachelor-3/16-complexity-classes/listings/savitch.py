"""savitch.py -- reachability with very little memory: is there a path from u to v of
length at most 2^k? Try every midpoint w, and ask the two halves recursively. Only the
current chain of calls is stored: k frames of (u, v, k, w)."""
import csv
import math
from collections import deque
from pathlib import Path


class Savitch:
    def __init__(self, n, edges):
        self.n, self.edges = n, set(edges)
        self.calls, self.depth, self.max_depth = 0, 0, 0

    def reach(self, u, v, k):
        self.calls += 1
        self.depth += 1
        self.max_depth = max(self.max_depth, self.depth)
        if k == 0:
            found = u == v or (u, v) in self.edges
        else:
            found = any(self.reach(u, w, k - 1) and self.reach(w, v, k - 1)
                        for w in range(self.n))
        self.depth -= 1
        return found

    def path_exists(self, u, v):
        return self.reach(u, v, max(1, math.ceil(math.log2(self.n))))


def bfs(n, edges, u, v):
    """The usual way: time O(n + m), but a queue and a set of up to n vertices."""
    adj = {x: [] for x in range(n)}
    for a, b in edges:
        adj[a].append(b)
    seen, queue = {u}, deque([u])
    while queue:
        x = queue.popleft()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                queue.append(y)
    return v in seen, len(seen)


if __name__ == "__main__":
    print("directed path 0 -> 1 -> ... -> n-1; from 0 to n-1, then back from n-1 to 0")
    print("  n   k   reachable  depth        calls   unreachable  depth        calls")
    for n in (2, 4, 8, 16):
        path = [(i, i + 1) for i in range(n - 1)]
        row = [n, max(1, math.ceil(math.log2(n)))]
        for u, v in ((0, n - 1), (n - 1, 0)):
            s = Savitch(n, path)
            row += [s.path_exists(u, v), s.max_depth, s.calls]
        line = "{:>3} {:>3}   {!s:>9} {:>6} {:>12,}   {!s:>11} {:>6} {:>12,}"
        print(line.format(*row))
    town = Path(__file__).resolve().parents[4] / "data" / "town" / "roads.csv"
    edges, roads, one_way = [], 0, 0
    for r in csv.DictReader(open(town)):
        a, b = int(r["from_place"]) - 1, int(r["to_place"]) - 1
        roads, one_way = roads + 1, one_way + (r["one_way"] == "1")
        edges += [(a, b)] if r["one_way"] == "1" else [(a, b), (b, a)]
    s = Savitch(30, edges)
    print(f"town: 30 places, {roads} roads ({one_way} one-way), {len(edges)} directed "
          f"edges")
    print(f"place 1 to place 30: {s.path_exists(0, 29)}, depth {s.max_depth}, "
          f"{s.calls:,} calls; BFS visits {bfs(30, edges, 0, 29)[1]} places")
