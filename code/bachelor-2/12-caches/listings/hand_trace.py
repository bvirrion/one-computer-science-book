"""hand_trace.py: a 256-byte direct-mapped cache, 16-byte lines, access by access."""
from cache import Cache

c = Cache(size=256, line=16, ways=1)
print("address  tag index offset  result")
for addr in [0x000, 0x004, 0x010, 0x100, 0x000, 0x110, 0x014, 0x200]:
    tag, index, offset = c.split(addr)
    hit = c.access(addr)
    print(f"{addr:#07x} {tag:>4} {index:>5} {offset:>6}  {'hit' if hit else 'miss'}")
print(f"{c.hits} hit, {c.misses} misses; valid sets:",
      {i: c.lines_in(i) for i in range(c.sets) if c.lines_in(i)})
