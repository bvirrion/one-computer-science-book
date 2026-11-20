"""ex5_split.py -- a B+ tree whose leaf split MOVES the middle key up, as an internal
split must, instead of copying it. Find a key it loses, and fix it."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from bptree import BPlusTree  # noqa: E402


class Buggy(BPlusTree):
    def split_leaf(self, pid):
        n, r = self.nodes[pid], self.new(leaf=True)
        right, half = self.nodes[r], len(self.nodes[pid].keys) // 2
        sep = n.keys[half]
        right.keys, right.kids = n.keys[half + 1 :], n.kids[half + 1 :]  # BUG
        n.keys, n.kids = n.keys[:half], n.kids[:half]
        right.next, n.next = n.next, r
        return sep, r


class Fixed(BPlusTree):
    pass  # the leaf split of bptree.py copies the key: it stays in the right leaf
