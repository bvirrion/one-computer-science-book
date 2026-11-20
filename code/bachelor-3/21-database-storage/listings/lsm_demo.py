"""lsm_demo.py -- 200,000 random writes into LSM trees with size ratios 4 and 10, then
lookups of present and absent keys: write amplification and runs read per lookup."""

import random

from lsm import LSM

rng = random.Random(21)
keys = [rng.randrange(10**9) for _ in range(200_000)]
for ratio in (4, 10):
    t = LSM(memtable=1000, ratio=ratio)
    for k in keys:
        t.put(k, k)
    sizes = [len(r.keys) if r else 0 for r in t.levels]
    print(f"T = {ratio}: levels {sizes}")
    print(
        f"  {t.inserted:,} writes, {t.written:,} entries written to disk: "
        f"write amplification {t.written / t.inserted:.1f}"
    )
    t.run_reads = 0
    assert all(t.get(k) == k for k in keys[:2000])
    hit = t.run_reads / 2000
    t.run_reads = 0
    assert all(t.get(-k - 1) is None for k in range(2000))
    print(
        f"  runs read per lookup: {hit:.2f} for present keys, "
        f"{t.run_reads / 2000:.3f} for absent keys"
    )
