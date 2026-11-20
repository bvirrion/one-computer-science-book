"""bloom_small.py: a Bloom filter of 16 bits with 3 hash functions, three names added,
two looked up."""
import random

from bloom import Bloom
from town import people


def key(name):  # a name as a number, byte by byte
    return int.from_bytes(name.encode(), "big") % (2**31 - 1)


f = Bloom(16, 3, random.Random(1))
for name in ["Ada", "Ben", "Cy"]:
    f.add(key(name))
    print(f"add {name:3}: bits {[h(key(name)) for h in f.hashes]}")
print("filter:", "".join(map(str, f.bits)))
others = sorted({p[1] for p in people()} - {"Ada", "Ben", "Cy"})
yes = [n for n in others if key(n) in f]
print(f"{len(others)} other first names looked up: {len(yes)} false positives")
for name in [others[0], yes[0]]:
    bits = [h(key(name)) for h in f.hashes]
    print(f"   {name}: bits {bits}, in filter: {key(name) in f}")
