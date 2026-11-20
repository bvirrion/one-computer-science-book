"""belady_search.py -- every reference string up to length 12, with any number of pages,
run under FIFO and LRU with 3 and with 4 frames: which ones fault more with 4?"""


def fifo_step(state, p, frames):  # state: (pages in arrival order, faults)
    pages, faults = state
    if p in pages:
        return state
    return (pages + (p,))[-frames:], faults + 1


def lru_step(state, p, frames):  # state: (pages, least recent first; faults)
    pages, faults = state
    rest = tuple(q for q in pages if q != p)
    return (rest + (p,))[-frames:], faults + (len(rest) == len(pages))


def search(n):
    """Strings of length n up to renaming: page k+1 first appears after page k."""
    found = {"strings": 0, "FIFO": [], "LRU": []}

    def extend(s, used, f3, f4, l3, l4):
        if len(s) == n:
            found["strings"] += 1
            if f4[1] > f3[1]:
                found["FIFO"].append(" ".join(map(str, s)))
            if l4[1] > l3[1]:
                found["LRU"].append(" ".join(map(str, s)))
            return
        for p in range(1, used + 2):  # an old page, or the next new one
            extend(s + [p], max(used, p), fifo_step(f3, p, 3), fifo_step(f4, p, 4),
                   lru_step(l3, p, 3), lru_step(l4, p, 4))

    empty = ((), 0)
    extend([], 0, empty, empty, empty, empty)
    return found


for n in range(1, 13):
    found = search(n)
    print(f"length {n:>2}: {found['strings']:>9,} strings, anomalous under FIFO "
          f"{len(found['FIFO'])}, under LRU {len(found['LRU'])}")
for s in found["FIFO"]:
    print(f"  {s}")
