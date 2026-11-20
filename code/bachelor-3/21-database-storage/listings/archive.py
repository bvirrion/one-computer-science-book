"""archive.py -- how tall is the town archive's index? Heights of a B+ tree from the
page format, then a measured tree of 1,000,000 keys and the cost of a lookup when
the top levels stay in the buffer pool."""

import random

from bptree import BPlusTree, bulk_load

PAGE, HEADER, KEY, PTR = 4096, 16, 8, 8
FANOUT = (PAGE - HEADER) // (KEY + PTR)  # children of an internal node
LEAF = FANOUT - 1  # entries of a leaf (key + 8-byte value)


def height(n, fill):
    """Levels needed for n keys when every node is filled to `fill`."""
    leaf, fan = int(LEAF * fill), int(FANOUT * fill)
    nodes, h = -(-n // leaf), 1
    while nodes > 1:
        nodes, h = -(-nodes // fan), h + 1
    return h


print(f"fan-out {FANOUT}, {LEAF} entries per leaf")
for n in (10**6, 10**9, 10**12):
    print(
        f"{n:>17,} keys: height {height(n, 1.0)} full, "
        f"{height(n, 0.69)} at 69 % fill, {height(n, 0.5)} half full"
    )

N = 1_000_000
keys = list(range(N))
random.Random(21).shuffle(keys)
grown = BPlusTree(FANOUT)
for k in keys:
    grown.insert(k, k)
loaded = bulk_load([(k, k) for k in range(N)], FANOUT)
for name, t in (("random inserts", grown), ("bulk loaded", loaded)):
    leaves = [n for n in t.nodes if n.leaf]
    fill = N / (len(leaves) * LEAF)
    t.reads = 0
    assert all(t.search(k) == k for k in keys[:1000])
    print(
        f"{name}: height {t.height()}, {len(t.nodes):,} pages, leaf fill {fill:.0%}, "
        f"{t.reads / 1000:.0f} reads per lookup"
    )

levels, pages = [], [loaded.root]
while pages:  # count the pages of each level of the bulk-loaded tree
    levels.append(len(pages))
    pages = [c for p in pages if not loaded.nodes[p].leaf for c in loaded.nodes[p].kids]
for cached in range(len(levels) + 1):
    size = sum(levels[:cached])
    mib = size * PAGE / 2**20
    print(
        f"{cached} top level(s) cached, {size:,} pages = {mib:.1f} MiB: "
        f"{len(levels) - cached} page read(s) per lookup"
    )
