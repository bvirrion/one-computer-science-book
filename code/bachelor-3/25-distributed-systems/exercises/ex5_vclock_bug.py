"""Exercise 5: a vector clock with a bug. The receive merges, but a receive is an event
too, and this version forgets to count it."""

PROCS = ["P1", "P2", "P3"]


def vector_clocks_buggy(run):
    clock = {p: [0] * len(PROCS) for p in PROCS}
    stamp, carried = {}, {}
    for e, p, kind, m in run:
        v = clock[p].copy()
        if kind == "recv":
            v = [max(x, y) for x, y in zip(v, carried[m])]
        else:
            v[PROCS.index(p)] += 1
        clock[p] = stamp[e] = v
        if kind == "send":
            carried[m] = v
    return stamp


def vector_clocks_fixed(run):
    clock = {p: [0] * len(PROCS) for p in PROCS}
    stamp, carried = {}, {}
    for e, p, kind, m in run:
        v = clock[p].copy()
        if kind == "recv":
            v = [max(x, y) for x, y in zip(v, carried[m])]
        v[PROCS.index(p)] += 1  # every event, receives included
        clock[p] = stamp[e] = v
        if kind == "send":
            carried[m] = v
    return stamp
