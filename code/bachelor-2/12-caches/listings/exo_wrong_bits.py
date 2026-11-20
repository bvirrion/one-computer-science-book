"""exo_wrong_bits.py: a simulator taking the index from the wrong bits (exercise 2)."""
from cache import Cache


class WrongCache(Cache):
    def split(self, addr):
        offset = addr & (self.line - 1)
        index = addr >> (32 - self.index_bits)       # the top bits of the address
        middle = 32 - self.index_bits - self.offset_bits  # the bits in between
        tag = (addr >> self.offset_bits) & ((1 << middle) - 1)
        return tag, index, offset


array = [0x10000000 + 4 * k for k in range(128)]    # 512 bytes, read twice
for cls in (Cache, WrongCache):
    c = cls(size=1024, line=32, ways=1)
    for addr in array + array:
        c.access(addr)
    print(f"{cls.__name__:<10} {c.hits:>4} hits {c.misses:>4} misses")
