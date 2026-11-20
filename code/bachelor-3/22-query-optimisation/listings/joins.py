"""joins.py -- five algorithms for the equi-join R.a = S.b, each counting page I/O
on a Disk (the result is returned, not written). M and N are the page counts of R
and S, B the buffer pages available."""

import sys
from collections import defaultdict
from pathlib import Path

from exec import materialise, merge, scan
from sort_ext import external_sort

sys.path.insert(
    0, str(Path(__file__).resolve().parents[2] / "21-database-storage" / "listings")
)
from bptree import BPlusTree  # noqa: E402


def nested_loop(R, S, a, b, disk):
    """For each tuple of R, scan all of S: M + |R| N."""
    return [merge(r, s) for r in scan(R, disk) for s in scan(S, disk) if r[a] == s[b]]


def block_nested_loop(R, S, a, b, B, disk):
    """Load B - 2 pages of R, hash them, scan S once per block: M + ceil(M/(B-2)) N."""
    out = []
    for start in range(0, len(R), B - 2):
        block = defaultdict(list)
        for page in R.pages[start : start + B - 2]:
            disk.reads += 1
            for r in page:
                block[r[a]].append(r)
        out += [merge(r, s) for s in scan(S, disk) for r in block.get(s[b], ())]
    return out


def build_index(S, b):
    """A B+ tree on S.b, a key of S; the values are (page, slot) record identifiers."""
    tree = BPlusTree(order=255)
    for p, page in enumerate(S.pages):
        for i, s in enumerate(page):
            tree.insert(s[b], (p, i))
    return tree


def index_nested_loop(R, S, a, b, tree, disk):
    """For each tuple of R, search the index (h page reads), then read the page of
    the matching tuple of S: M + |R| (h + 1) when every tuple matches."""
    out = []
    for r in scan(R, disk):
        tree.reads = 0
        rid = tree.search(r[a])
        disk.reads += tree.reads
        if rid is not None:
            disk.reads += 1
            out.append(merge(r, S.pages[rid[0]][rid[1]]))
    return out


def sort_merge(R, S, a, b, B, disk):
    """Sort both, then merge; S.b is a key of S, as in a foreign-key join."""
    Rs, _ = external_sort(R, lambda t: t[a], B, disk)
    Ss, _ = external_sort(S, lambda t: t[b], B, disk)
    out, it = [], scan(Ss, disk)
    s = next(it, None)
    for r in scan(Rs, disk):
        while s is not None and s[b] < r[a]:
            s = next(it, None)
        if s is not None and s[b] == r[a]:
            out.append(merge(r, s))
    for _ in it:  # read the rest of S, as a merge does
        pass
    return out


def hash_join(R, S, a, b, B, disk):
    """Build a hash table on the smaller input if it fits in B - 2 pages: M + N.
    Otherwise partition both into B - 1 buckets on disk first (Grace): 3(M + N)."""
    if len(R) < len(S):
        R, S, a, b, swapped = S, R, b, a, True
    else:
        swapped = False
    pairs = [(R, S)]
    if len(S) > B - 2:
        pairs = list(zip(partition(R, a, B, disk), partition(S, b, B, disk)))
    out = []
    for Rp, Sp in pairs:
        table = defaultdict(list)
        for s in scan(Sp, disk):
            table[s[b]].append(s)
        for r in scan(Rp, disk):
            out += [
                merge(s, r) if swapped else merge(r, s) for s in table.get(r[a], ())
            ]
    return out


def partition(rel, key, B, disk):
    buckets = [[] for _ in range(B - 1)]
    for t in scan(rel, disk):
        buckets[hash(t[key]) % (B - 1)].append(t)
    return [materialise(bucket, disk, rel.per_page) for bucket in buckets]
