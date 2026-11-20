"""exo_rank_bug.py: exercise 6, union by rank that raises the wrong rank."""

from union_find import UnionFind


class Buggy(UnionFind):
    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[ry] += 1
        return True


def tallest(uf):
    def height(x):
        h = 0
        while uf.parent[x] != x:
            x, h = uf.parent[x], h + 1
        return h
    return max(map(height, uf.parent))


if __name__ == "__main__":
    for kind in (UnionFind, Buggy):
        s = kind(range(1000))
        for i in range(1, 1000):
            s.union(i, i - 1)
        top = max(s.rank[x] for x in s.parent if s.parent[x] == x)
        print(f"{kind.__name__:9} tallest tree {tallest(s):3}, root rank {top}")
