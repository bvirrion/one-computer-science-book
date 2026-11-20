"""lpm_bench.py: lookup time against table size, linear scan and trie (laptop)."""
import random
import time

import lpm_linear
from cidr import dotted
from lpm_trie import Trie

rng = random.Random(18)


def random_table(n):
    prefixes = {"0.0.0.0/0"}
    while len(prefixes) < n:                   # n different prefixes
        length = rng.randrange(8, 25)
        net = rng.getrandbits(length) << (32 - length)
        prefixes.add(f"{dotted(net)}/{length}")
    return [(p, k) for k, p in enumerate(sorted(prefixes))]


print("prefixes  linear (us/lookup)  trie (us/lookup)")
for n in (250, 1000, 4000):
    table = random_table(n)
    trie = Trie()
    for prefix, hop in table:
        trie.insert(prefix, hop)
    addrs = [dotted(rng.getrandbits(32)) for _ in range(500)]
    t0 = time.perf_counter()
    a = [lpm_linear.lookup(table, x) for x in addrs]
    t1 = time.perf_counter()
    b = [trie.lookup(x)[0] for x in addrs]
    t2 = time.perf_counter()
    assert a == b
    print(f"{n:8} {(t1 - t0) / 500 * 1e6:19.0f} {(t2 - t1) / 500 * 1e6:17.1f}")
