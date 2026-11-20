"""lsm.py -- a log-structured merge tree with levelled compaction. Writes go to a
memtable; a full memtable is written out as a sorted run at level 0; when level i
holds more than C * T^(i+1) entries it is merged into level i + 1, which is
rewritten. Each run has a Bloom filter, so a lookup reads only the runs that may
hold the key. Entries written to disk are counted."""

import hashlib
from bisect import bisect_left


class Bloom:
    def __init__(self, keys, bits_per_key=10, k=7):
        self.m, self.k = max(8, bits_per_key * len(keys)), k
        self.bits = bytearray(self.m // 8 + 1)
        for key in keys:
            for p in self.positions(key):
                self.bits[p // 8] |= 1 << p % 8

    def positions(self, key):
        d = hashlib.blake2b(str(key).encode(), digest_size=16).digest()
        a, b = int.from_bytes(d[:8], "little"), int.from_bytes(d[8:], "little")
        return [(a + i * b) % self.m for i in range(self.k)]

    def may_contain(self, key):
        return all(self.bits[p // 8] >> p % 8 & 1 for p in self.positions(key))


class Run:
    def __init__(self, items):
        self.keys, self.values = [k for k, _ in items], [v for _, v in items]
        self.bloom = Bloom(self.keys)


class LSM:
    def __init__(self, memtable=1000, ratio=10):
        self.C, self.T, self.mem, self.levels = memtable, ratio, {}, []
        self.inserted = self.written = self.run_reads = 0

    def put(self, key, value):
        self.inserted += 1
        self.mem[key] = value
        if len(self.mem) >= self.C:
            self.push(0, sorted(self.mem.items()))
            self.mem = {}

    def push(self, i, items):
        """Merge items into level i (newer wins), write the level, cascade if over."""
        if i == len(self.levels):
            self.levels.append(None)
        old = self.levels[i]
        merged = dict(zip(old.keys, old.values)) if old else {}
        merged.update(items)
        run = sorted(merged.items())
        self.written += len(run)  # the whole level is rewritten
        if len(run) > self.C * self.T ** (i + 1):
            self.levels[i] = None
            self.push(i + 1, run)
        else:
            self.levels[i] = Run(run)

    def get(self, key):
        if key in self.mem:
            return self.mem[key]
        for run in self.levels:  # newest level first
            if run and run.bloom.may_contain(key):
                self.run_reads += 1
                j = bisect_left(run.keys, key)
                if j < len(run.keys) and run.keys[j] == key:
                    return run.values[j]
        return None
