"""exo_skiplist.py: a skip list; each key is promoted one level up with probability 1/2.
The nodes looked at by a search, against log2 n."""
import math
import random


class SkipList:
    def __init__(self, rng):
        self.rng = rng
        self.head = [None]  # head[i]: the first node of level i
        # a node is [key, next at level 0, next at level 1, ...]

    def search(self, key):
        """The largest key <= key at level 0, and the number of nodes looked at."""
        level, node, looked = len(self.head) - 1, None, 0
        while level >= 0:
            nxt = (node[level + 1] if node else self.head[level])
            while nxt is not None and nxt[0] <= key:
                node, looked = nxt, looked + 1
                nxt = node[level + 1]
            looked += 1  # the node that stopped us, or the end of the level
            level -= 1
        return node, looked

    def insert(self, key):
        height = 1
        while self.rng.random() < 0.5:
            height += 1
        while len(self.head) < height:
            self.head.append(None)
        new = [key] + [None] * height
        level, node = len(self.head) - 1, None
        while level >= 0:
            nxt = node[level + 1] if node else self.head[level]
            while nxt is not None and nxt[0] < key:
                node, nxt = nxt, nxt[level + 1]
            if level < height:  # link the new node in at this level
                new[level + 1] = nxt
                if node:
                    node[level + 1] = new
                else:
                    self.head[level] = new
            level -= 1


rng = random.Random(14)
print("      n  levels  nodes looked at (mean of 1,000 searches)  2 log2 n")
for e in range(10, 17, 2):
    n = 2**e
    s = SkipList(rng)
    for key in rng.sample(range(10 * n), n):
        s.insert(key)
    looked = [s.search(rng.randrange(10 * n))[1] for _ in range(1000)]
    print(f"{n:7} {len(s.head):7} {sum(looked) / 1000:42.1f} {2 * math.log2(n):9.1f}")
