"""cache.py: a set-associative cache with LRU replacement and two write policies."""
from collections import OrderedDict


class Cache:
    """size and line in bytes; ways = 1 is direct-mapped, ways = size // line is fully
    associative. write_back: dirty lines are written to memory when evicted;
    otherwise every store goes to memory at once (write-through)."""

    def __init__(self, size, line, ways, write_back=True, write_allocate=True):
        self.line, self.ways = line, ways
        self.sets = size // (line * ways)
        self.offset_bits = line.bit_length() - 1
        self.index_bits = self.sets.bit_length() - 1
        self.write_back, self.write_allocate = write_back, write_allocate
        self.data = [OrderedDict() for _ in range(self.sets)]  # tag -> dirty, LRU first
        self.hits = self.misses = self.memory_writes = 0

    def split(self, addr):
        """(tag, index, offset) of an address."""
        offset = addr & (self.line - 1)
        index = (addr >> self.offset_bits) & (self.sets - 1)
        tag = addr >> (self.offset_bits + self.index_bits)
        return tag, index, offset

    def access(self, addr, write=False):
        """One load or store; returns True on a hit."""
        tag, index, _ = self.split(addr)
        s = self.data[index]
        if tag in s:
            self.hits += 1
            s.move_to_end(tag)                      # now the most recently used
            if write:
                s[tag] = s[tag] or self.write_back
                self.memory_writes += not self.write_back
            return True
        self.misses += 1
        if write and not self.write_allocate:
            self.memory_writes += 1                  # the store goes around the cache
            return False
        if len(s) == self.ways:
            _, dirty = s.popitem(last=False)         # evict the least recently used
            self.memory_writes += dirty
        s[tag] = write and self.write_back
        self.memory_writes += write and not self.write_back
        return False

    def lines_in(self, index):
        """The tags of a set, least recently used first."""
        return list(self.data[index])

    def miss_ratio(self):
        return self.misses / (self.hits + self.misses)
