"""bptree_demo.py -- 100,000 keys in a B+ tree whose order comes from the page format:
a 4,096-byte page, a 16-byte node header, 8-byte keys and 8-byte page numbers."""

import random

from bptree import BPlusTree, bulk_load

ORDER = (4096 - 16) // 16  # children per internal node: 255
N = 100_000

keys = list(range(N))
random.Random(21).shuffle(keys)
for name in ("random inserts", "bulk loaded"):
    if name == "random inserts":
        t = BPlusTree(ORDER)
        for k in keys:
            t.insert(k, -k)
    else:
        t = bulk_load([(k, -k) for k in range(N)], ORDER)
    leaves = sum(n.leaf for n in t.nodes)
    print(
        f"{name}: order {ORDER}, height {t.height()}, {len(t.nodes):,} pages, "
        f"{leaves:,} leaves, {N / leaves:.0f} keys per leaf"
    )
    t.reads = 0
    assert all(t.search(k) == -k for k in keys[:1000])
    print(f"  1,000 lookups: {t.reads:,} page reads, {t.reads / 1000:.0f} per lookup")
    t.reads = 0
    found = sum(1 for _ in t.range(50_000, 60_000))
    print(f"  range [50000, 60000): {found:,} keys in {t.reads} page reads")

small = BPlusTree(4)
for k in (5, 15, 25, 35, 45, 20, 30, 10, 40, 50):
    small.insert(k, None)
print("order 4 after 10 inserts: height", small.height())
for pid, n in enumerate(small.nodes):
    print(
        f"  page {pid}: {'leaf' if n.leaf else 'node'} {n.keys}"
        + ("" if n.leaf else f" -> pages {n.kids}")
    )
print("  root is page", small.root)
