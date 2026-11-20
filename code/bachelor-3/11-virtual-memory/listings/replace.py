"""replace.py -- four page replacement policies counting faults on reference strings."""
from collections import OrderedDict


def fifo(refs, frames):
    resident, faults = [], 0
    for p in refs:
        if p not in resident:
            faults += 1
            if len(resident) == frames:
                resident.pop(0)  # the page that came in first
            resident.append(p)
    return faults


def lru(refs, frames):
    resident, faults = OrderedDict(), 0  # least recently used first
    for p in refs:
        if p in resident:
            resident.move_to_end(p)
            continue
        faults += 1
        if len(resident) == frames:
            resident.popitem(last=False)
        resident[p] = True
    return faults


def clock(refs, frames):
    page, ref, hand, faults = [None] * frames, [0] * frames, 0, 0
    for p in refs:
        if p in page:
            ref[page.index(p)] = 1  # the hardware sets the referenced bit
            continue
        faults += 1
        while ref[hand]:  # a second chance: clear the bit, move on
            ref[hand], hand = 0, (hand + 1) % frames
        page[hand], ref[hand], hand = p, 1, (hand + 1) % frames
    return faults


def opt(refs, frames):
    resident, faults = set(), 0
    for t, p in enumerate(refs):
        if p in resident:
            continue
        faults += 1
        if len(resident) == frames:  # evict the page needed furthest in the future
            later = refs[t + 1:]
            next_use = {q: later.index(q) if q in later else len(later)
                        for q in resident}
            resident.remove(max(resident, key=next_use.get))
        resident.add(p)
    return faults


POLICIES = {"FIFO": fifo, "LRU": lru, "clock": clock, "OPT": opt}
if __name__ == "__main__":
    for name, refs in (("Belady's string", [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]),
                       ("a loop over 5 pages, 3 times", [1, 2, 3, 4, 5] * 3)):
        print(f"{name}: {' '.join(map(str, refs))}")
        print("frames " + "".join(f"{f:>4}" for f in range(1, 6)))
        for pname, policy in POLICIES.items():
            counts = "".join(f"{policy(refs, f):>4}" for f in range(1, 6))
            print(f"{pname:<6} {counts}")
