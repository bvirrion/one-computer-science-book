"""bptree.py -- a B+ tree whose nodes are pages: every node visited is one page read.
Order m: an internal node has at most m children, a leaf at most m - 1 keys; leaves
are chained left to right for range scans."""

from bisect import bisect_left, bisect_right


class Node:
    def __init__(self, leaf):
        self.leaf, self.keys, self.kids, self.next = leaf, [], [], None  # kids: values


class BPlusTree:
    def __init__(self, order):
        self.m, self.nodes, self.reads, self.writes = order, [], 0, 0
        self.root = self.new(leaf=True)

    def new(self, leaf):
        self.nodes.append(Node(leaf))
        self.writes += 1
        return len(self.nodes) - 1

    def node(self, pid):
        self.reads += 1  # one page read per node visited
        return self.nodes[pid]

    def leaf_for(self, key):
        n = self.node(self.root)
        while not n.leaf:
            n = self.node(n.kids[bisect_right(n.keys, key)])
        return n

    def search(self, key):
        n = self.leaf_for(key)
        i = bisect_left(n.keys, key)
        return n.kids[i] if i < len(n.keys) and n.keys[i] == key else None

    def range(self, lo, hi):
        """Every (key, value) with lo <= key < hi, following the leaf chain."""
        n = self.leaf_for(lo)
        while True:
            for k, v in zip(n.keys, n.kids):
                if k >= hi:
                    return
                if k >= lo:
                    yield k, v
            if n.next is None:
                return
            n = self.node(n.next)

    def insert(self, key, value):
        split = self._insert(self.root, key, value)
        if split:  # the root split: a new root one level up
            sep, right = split
            root = self.new(leaf=False)
            self.nodes[root].keys, self.nodes[root].kids = [sep], [self.root, right]
            self.root = root

    def _insert(self, pid, key, value):
        n = self.node(pid)
        if n.leaf:
            i = bisect_left(n.keys, key)
            if i < len(n.keys) and n.keys[i] == key:
                n.kids[i] = value  # replace
                return None
            n.keys.insert(i, key)
            n.kids.insert(i, value)
            self.writes += 1
            return self.split_leaf(pid) if len(n.keys) > self.m - 1 else None
        i = bisect_right(n.keys, key)
        split = self._insert(n.kids[i], key, value)
        if split:
            sep, right = split
            n.keys.insert(i, sep)
            n.kids.insert(i + 1, right)
            self.writes += 1
            return self.split_internal(pid) if len(n.kids) > self.m else None
        return None

    def split_leaf(self, pid):
        """The upper half moves to a new leaf; its first key is COPIED up."""
        n, r = self.nodes[pid], self.new(leaf=True)
        right, half = self.nodes[r], len(self.nodes[pid].keys) // 2
        right.keys, right.kids = n.keys[half:], n.kids[half:]
        n.keys, n.kids = n.keys[:half], n.kids[:half]
        right.next, n.next = n.next, r
        return right.keys[0], r

    def split_internal(self, pid):
        """The middle key MOVES up: it stays in neither half."""
        n, r = self.nodes[pid], self.new(leaf=False)
        right, half = self.nodes[r], len(self.nodes[pid].keys) // 2
        sep = n.keys[half]
        right.keys, right.kids = n.keys[half + 1 :], n.kids[half + 1 :]
        n.keys, n.kids = n.keys[:half], n.kids[: half + 1]
        return sep, r

    def height(self):
        h, n = 1, self.nodes[self.root]
        while not n.leaf:
            h, n = h + 1, self.nodes[n.kids[0]]
        return h


def chunks(seq, cap):
    """Cut seq into as few pieces of at most cap as possible, of near-equal sizes, so
    that no piece is less than half full."""
    g = -(-len(seq) // cap)
    cuts = [len(seq) * j // g for j in range(g + 1)]
    return [seq[a:b] for a, b in zip(cuts, cuts[1:])]


def bulk_load(items, order, fill=1.0):
    """Build the tree bottom up from sorted (key, value) pairs: leaves, then each
    level of separators, without a single split."""
    t = BPlusTree(order)
    t.nodes, t.writes, level = [], 0, []
    for group in chunks(items, max(1, int((order - 1) * fill))):
        pid = t.new(leaf=True)
        t.nodes[pid].keys = [k for k, _ in group]
        t.nodes[pid].kids = [v for _, v in group]
        if level:
            t.nodes[level[-1][1]].next = pid
        level.append((group[0][0], pid))
    while len(level) > 1:
        upper = []
        for group in chunks(level, max(2, int(order * fill))):
            pid = t.new(leaf=False)
            t.nodes[pid].keys = [k for k, _ in group[1:]]
            t.nodes[pid].kids = [p for _, p in group]
            upper.append((group[0][0], pid))
        level = upper
    t.root = level[0][1] if level else t.new(leaf=True)
    return t
