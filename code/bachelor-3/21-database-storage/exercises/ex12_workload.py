"""ex12_workload.py -- the B+ tree and the LSM tree under a read-heavy and a
write-heavy workload of 100,000 operations, counted in page I/O. B+ tree: nodes
read and nodes written. LSM: one page read per run searched (its index and
Bloom filter in memory), entries written / 254 per page written."""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from bptree import BPlusTree  # noqa: E402
from lsm import LSM  # noqa: E402

PER_PAGE = 254


def workload(read_share, n=100_000, seed=21):
    rng, keys, ops = random.Random(seed), [], []
    for _ in range(n):
        if keys and rng.random() < read_share:
            ops.append(("get", rng.choice(keys)))
        else:
            keys.append(rng.randrange(10**9))
            ops.append(("put", keys[-1]))
    return ops


def run(ops):
    tree, lsm = BPlusTree(255), LSM(memtable=1000, ratio=10)
    for op, k in ops:
        if op == "put":
            tree.insert(k, k)
            lsm.put(k, k)
        else:
            tree.search(k)
            lsm.get(k)
    return (tree.reads + tree.writes) / len(ops), (
        lsm.run_reads + lsm.written / PER_PAGE
    ) / len(ops)


if __name__ == "__main__":
    for name, share in (
        ("read-heavy (90 % reads)", 0.9),
        ("write-heavy (10 % reads)", 0.1),
    ):
        b, s = run(workload(share))
        print(f"{name}: B+ tree {b:.2f}, LSM {s:.2f} page I/O per operation")
