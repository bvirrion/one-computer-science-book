"""extendible.py -- extendible hashing: a directory of 2^d pointers to buckets, indexed
by the last d bits of the hash. A full bucket splits on one more bit; when its local
depth already equals d, the directory doubles first."""


class Extendible:
    def __init__(self, capacity, h=hash):
        self.cap, self.h, self.depth = capacity, h, 0
        self.dir = [{"depth": 0, "items": {}}]  # bucket objects, shared by pointers
        self.doublings = self.splits = 0

    def bucket(self, key):
        return self.dir[self.h(key) & ((1 << self.depth) - 1)]

    def get(self, key):
        return self.bucket(key)["items"].get(key)

    def put(self, key, value):
        b = self.bucket(key)
        if key in b["items"] or len(b["items"]) < self.cap:
            b["items"][key] = value
            return
        if b["depth"] == self.depth:  # no spare bit: double the directory
            self.dir += self.dir
            self.depth += 1
            self.doublings += 1
        bit = 1 << b["depth"]  # split b on its next bit
        b["depth"] += 1
        new = {"depth": b["depth"], "items": {}}
        for k in [k for k in b["items"] if self.h(k) & bit]:
            new["items"][k] = b["items"].pop(k)
        for i in range(len(self.dir)):
            if self.dir[i] is b and i & bit:
                self.dir[i] = new
        self.splits += 1
        self.put(key, value)  # may split again


def label(i, b):
    """A bucket named by the low bits its keys share: d = 2, i = 6 gives "10"."""
    d = b["depth"]
    return format(i & ((1 << d) - 1), f"0{d}b") if d else "*"


if __name__ == "__main__":
    e = Extendible(capacity=2, h=lambda k: k)
    for k in (4, 9, 16, 1, 25, 12, 7, 20):
        before = e.depth
        e.put(k, str(k))
        seen = {id(b): (label(i, b), sorted(b["items"])) for i, b in enumerate(e.dir)}
        grew = f" x{2 ** (e.depth - before)}" if e.depth > before else ""
        shown = " ".join(f"{bits}:{items}" for bits, items in sorted(seen.values()))
        print(f"put {k:>2} = {k:05b}: d = {e.depth}{grew:<4} {shown}")
    big = Extendible(capacity=64)
    for k in range(100_000):
        big.put(k * 2654435761 % 2**32, k)
    print(
        f"100,000 keys, 64 per bucket: directory 2^{big.depth} = {len(big.dir):,}, "
        f"{len({id(b) for b in big.dir}):,} buckets, {big.doublings} doublings"
    )
