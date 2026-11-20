"""ex11_linear.py -- linear hashing: buckets split one at a time, in order, whenever
the load passes a threshold; no directory. Bucket i uses h_L(k) = k mod (N * 2^L)
unless it has already been split this round (i < next), then h_{L+1}. A bucket
holds `cap` keys in its primary page; more spill into overflow pages."""


class LinearHash:
    def __init__(self, n=4, cap=4, max_load=0.8):
        self.N, self.cap, self.max_load = n, cap, max_load
        self.level, self.next, self.buckets, self.size = 0, 0, [{} for _ in range(n)], 0

    def address(self, key):
        h = hash(key)
        i = h % (self.N << self.level)
        return h % (self.N << (self.level + 1)) if i < self.next else i

    def get(self, key):
        return self.buckets[self.address(key)].get(key)

    def put(self, key, value):
        b = self.buckets[self.address(key)]
        self.size += key not in b
        b[key] = value
        while self.size > self.max_load * self.cap * len(self.buckets):
            self.split()

    def split(self):
        """Split bucket `next` (not necessarily the one that overflowed)."""
        old = self.buckets[self.next]
        self.buckets.append({})
        self.next += 1
        self.buckets[self.next - 1] = {}
        for k, v in old.items():
            self.buckets[self.address(k)][k] = v
        if self.next == self.N << self.level:  # round over: every bucket split
            self.level, self.next = self.level + 1, 0

    def overflow_pages(self):
        return sum(max(0, -(-len(b) // self.cap) - 1) for b in self.buckets)
