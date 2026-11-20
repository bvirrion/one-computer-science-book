"""union_find.py: disjoint sets with union by rank and path compression; the parent
pointers followed are counted."""


class UnionFind:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}
        self.steps = 0  # parent pointers followed by find

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
            self.steps += 1
        while self.parent[x] != root:  # path compression: point straight at the root
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x, y):
        """Merge the sets of x and y; False if they were already one set."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx  # the shorter tree goes under the taller
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


if __name__ == "__main__":
    for n in (100, 1000, 10000):
        s = UnionFind(range(n))
        for i in range(1, n):  # the chain of uf_naive.py
            s.union(i, 0)
            s.find(0)
        print(f"n = {n:5}: {s.steps:5} steps, largest rank {max(s.rank.values())}")
