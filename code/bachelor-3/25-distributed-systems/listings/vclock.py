"""vclock.py -- vector clocks on the run of lamport.py. Process i keeps one counter per
process: it adds 1 to its own entry at every event, and on a receive first takes the
entrywise maximum with the vector the message carries."""

from lamport import RUN, happened_before

PROCS = ["P1", "P2", "P3"]


def vector_clocks(run):
    clock = {p: [0] * len(PROCS) for p in PROCS}
    stamp, carried = {}, {}
    for e, p, kind, m in run:
        v = clock[p]
        if kind == "recv":
            v = [max(x, y) for x, y in zip(v, carried[m])]
        v = v.copy()
        v[PROCS.index(p)] += 1
        clock[p] = stamp[e] = v
        if kind == "send":
            carried[m] = v
    return stamp


def before(u, v):
    """u < v: no entry larger, and the vectors differ."""
    return all(x <= y for x, y in zip(u, v)) and u != v


if __name__ == "__main__":
    V, hb = vector_clocks(RUN), happened_before(RUN)
    for p in PROCS:
        print(p, "  ".join(f"{e}:{V[e]}" for e, q, _, _ in RUN if q == p))
    events = [e for e, *_ in RUN]
    exact = all(before(V[e], V[f]) == ((e, f) in hb) for e in events for f in events)
    print(
        f"V(e) < V(f) exactly when e -> f, over all {len(events) ** 2} pairs: {exact}"
    )
    conc = [
        (e, f)
        for i, e in enumerate(events)
        for f in events[i + 1 :]
        if not before(V[e], V[f]) and not before(V[f], V[e])
    ]
    print(f"{len(conc)} concurrent pairs:", " ".join(f"{e}||{f}" for e, f in conc))
