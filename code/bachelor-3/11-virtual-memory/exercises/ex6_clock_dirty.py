"""ex6_clock_dirty.py -- clock with a dirty bit: prefer to evict a page that is neither
referenced nor dirty, so that fewer evictions must write the page back to disk."""


def clock_dirty(refs, frames):
    """refs: (page, 'r' or 'w'). Returns (faults, write-backs)."""
    page, ref, dirty = [None] * frames, [0] * frames, [0] * frames
    hand = faults = writes = 0
    for p, op in refs:
        if p in page:
            i = page.index(p)
        else:
            faults += 1
            if None in page:
                i = page.index(None)
            else:
                i = victim(ref, dirty, hand)
                writes += dirty[i]
                hand = (i + 1) % frames
            page[i], dirty[i] = p, 0
        ref[i] = 1
        dirty[i] |= op == "w"
    return faults, writes


def victim(ref, dirty, hand):
    n = len(ref)
    while True:
        for k in range(n):  # pass 1: a clean page not referenced; change nothing
            i = (hand + k) % n
            if not ref[i] and not dirty[i]:
                return i
        for k in range(n):  # pass 2: a dirty page not referenced; clear the bits passed
            i = (hand + k) % n
            if not ref[i]:
                return i
            ref[i] = 0


def clock_writes(refs, frames):
    """Plain clock on the same references, counting its write-backs too."""
    page, ref, dirty = [None] * frames, [0] * frames, [0] * frames
    hand = faults = writes = 0
    for p, op in refs:
        if p in page:
            i = page.index(p)
        else:
            faults += 1
            while ref[hand]:
                ref[hand], hand = 0, (hand + 1) % frames
            i, hand = hand, (hand + 1) % frames
            writes += dirty[i] if page[i] is not None else 0
            page[i], dirty[i] = p, 0
        ref[i] = 1
        dirty[i] |= op == "w"
    return faults, writes
