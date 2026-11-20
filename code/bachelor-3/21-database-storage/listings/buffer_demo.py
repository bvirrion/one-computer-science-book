"""buffer_demo.py -- hit rate of the buffer pool against its size, on a seeded access
pattern over 1,000 pages: 80 % of the accesses go to 20 % of the pages."""

import random

from bufferpool import BufferPool
from pagefile import PageFile

file = PageFile()
for _ in range(1000):
    file.allocate()
rng = random.Random(21)
hot = rng.sample(range(1000), 200)
trace = [
    rng.choice(hot) if rng.random() < 0.8 else rng.randrange(1000)
    for _ in range(50_000)
]
print("frames   hit rate   page reads   page writes")
for frames in (10, 50, 100, 200, 400, 1000):
    pool, file.reads, file.writes = BufferPool(file, frames), 0, 0
    for i, pid in enumerate(trace):
        pool.fetch(pid)
        pool.unpin(pid, dirty=i % 10 == 0)  # one access in ten changes the page
    pool.flush()
    print(
        f"{frames:>6}   {pool.hits / len(trace):>7.1%}   {file.reads:>10,}"
        f"   {file.writes:>11,}"
    )
