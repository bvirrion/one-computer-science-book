"""probes.py: counted probes per successful and unsuccessful search, as the load factor
grows, for chaining and linear probing; random hash values (seeded), m = 10007."""

import random
from pathlib import Path

M = 10007
rng = random.Random(16)


def chaining(alpha):
    n = int(alpha * M)
    sizes, hit = [0] * M, 0
    for _ in range(n):
        b = rng.randrange(M)
        sizes[b] += 1
        hit += sizes[b]  # a later search for this key compares sizes[b] keys
    miss = sum(sizes) / M  # an absent key walks a whole chain
    return hit / n, miss


def probing(alpha):
    n = int(alpha * M)
    used, hit = [False] * M, 0
    for _ in range(n):
        i, p = rng.randrange(M), 1
        while used[i]:
            i, p = (i + 1) % M, p + 1
        used[i] = True
        hit += p  # a search for this key probes the same slots
    miss = 0
    for i in range(M):  # an absent key with hash i probes up to the next free slot
        j = i
        while used[j]:
            j = (j + 1) % M
        miss += (j - i) % M + 1
    return hit / n, miss / M


with open(Path(__file__).resolve().parent / "probes.dat", "w") as f:
    f.write("alpha chainhit chainmiss probehit probemiss\n")
    for k in range(1, 20):
        a = k / 20
        (ch, cm), (ph, pm) = chaining(a), probing(a)
        f.write(f"{a:.2f} {ch:.3f} {cm:.3f} {ph:.3f} {pm:.3f}\n")
