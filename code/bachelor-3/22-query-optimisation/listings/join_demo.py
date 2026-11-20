"""join_demo.py -- the five joins on generated tables: 10,000 loans (1,000 pages)
referring to 1,000 books (100 pages, book_id a key), with 12 buffer pages."""

import random

from exec import Disk, Relation
from joins import (
    block_nested_loop,
    build_index,
    hash_join,
    index_nested_loop,
    nested_loop,
    sort_merge,
)
from sort_ext import formula

rng = random.Random(22)
R = Relation({"loan": i, "book": rng.randrange(1000)} for i in range(10_000))
S = Relation({"book_id": j, "pages": rng.randrange(40, 400)} for j in range(1000))
M, N, B, n = len(R), len(S), 12, 10_000
tree = build_index(S, "book_id")
plans = [
    ("nested loop", lambda d: nested_loop(R, S, "book", "book_id", d), M + n * N),
    (
        "block nested loop",
        lambda d: block_nested_loop(R, S, "book", "book_id", B, d),
        M + -(-M // (B - 2)) * N,
    ),
    (
        "index nested loop",
        lambda d: index_nested_loop(R, S, "book", "book_id", tree, d),
        M + n * (tree.height() + 1),
    ),
    (
        "sort-merge",
        lambda d: sort_merge(R, S, "book", "book_id", B, d),
        formula(M, B) + formula(N, B) + M + N,
    ),
    ("hash (Grace)", lambda d: hash_join(R, S, "book", "book_id", B, d), 3 * (M + N)),
]
print(f"M = {M} pages, N = {N} pages, B = {B}, index height {tree.height()}")
print("join                 result   page I/O   formula")
for name, run, cost in plans:
    disk = Disk()
    rows = run(disk)
    print(f"{name:<18} {len(rows):>8,} {disk.io():>10,} {cost:>9,}")
