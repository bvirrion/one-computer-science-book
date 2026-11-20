"""birthday.py -- a 32-bit checksum: the first 4 bytes of SHA-256. Hash distinct
records until two checksums collide, in 200 runs with different record prefixes, and
compare the mean with sqrt(pi/2 * 2^32)."""

import hashlib
import math


def first_collision(run):
    seen, i = {}, 0
    while True:
        record = f"run {run} record {i}".encode()
        h = hashlib.sha256(record).digest()[:4]
        if h in seen:
            return i + 1, seen[h], record
        seen[h] = record
        i += 1


counts = []
for run in range(200):
    n, a, b = first_collision(run)
    counts.append(n)
    if run == 0:
        print(
            f"run 0: {a.decode()!r} and {b.decode()!r} share",
            hashlib.sha256(a).digest()[:4].hex(),
        )
print("first ten runs, hashes until a collision:", " ".join(map(str, counts[:10])))
print(f"fewest {min(counts):,}, most {max(counts):,}")
mean = sum(counts) / len(counts)
expect = math.sqrt(math.pi / 2 * 2**32)
print(f"mean of 200 runs {mean:,.0f}; sqrt(pi/2 * 2^32) = {expect:,.0f}")
print(f"ratio {mean / expect:.3f}")
