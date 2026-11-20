"""sort_ext.py -- external merge sort with B buffer pages. Pass 0 reads B pages at a
time, sorts them in memory and writes a run; each later pass merges B - 1 runs into
one, until a single run is left. Every pass reads and writes every page."""

import heapq
import math
import random

from exec import Disk, Relation, materialise


def external_sort(rel, key, B, disk):
    runs = []
    for s in range(0, len(rel), B):  # pass 0: sorted runs of B pages
        chunk = [t for page in rel.pages[s : s + B] for t in page]
        disk.reads += len(rel.pages[s : s + B])
        runs.append(materialise(sorted(chunk, key=key), disk, rel.per_page))
    passes = 1
    while len(runs) > 1:  # merge B - 1 runs at a time, one output buffer
        merged = []
        for s in range(0, len(runs), B - 1):
            group = runs[s : s + B - 1]
            streams = [scan_run(r, disk) for r in group]
            merged.append(
                materialise(heapq.merge(*streams, key=key), disk, rel.per_page)
            )
        runs, passes = merged, passes + 1
    return (runs[0] if runs else Relation([], rel.per_page)), passes


def scan_run(run, disk):
    for page in run.pages:
        disk.reads += 1
        yield from page


def formula(N, B):
    """2N(1 + ceil(log_{B-1} ceil(N/B))), the logarithm counted in integers."""
    runs, merges = math.ceil(N / B), 0
    while runs > 1:
        runs, merges = math.ceil(runs / (B - 1)), merges + 1
    return 2 * N * (1 + merges)


if __name__ == "__main__":
    rng = random.Random(22)
    print("pages N  buffers B  passes  page I/O  2N(1 + ceil(log_{B-1} ceil(N/B)))")
    for N in (10, 100, 1000, 10_000):
        rel = Relation([{"k": rng.random()} for _ in range(10 * N)])
        for B in (3, 10, 100):
            disk = Disk()
            out, passes = external_sort(rel, lambda t: t["k"], B, disk)
            assert [t["k"] for t in out.rows()] == sorted(t["k"] for t in rel.rows())
            print(
                f"{N:>7,}  {B:>9}  {passes:>6}  {disk.io():>8,}  {formula(N, B):>10,}"
            )
