"""lamport.py -- Lamport clocks on a recorded run of three processes. Each process
ticks its clock at every event; a message carries the sender's clock, and a receive
sets the clock to one more than the larger of its own and the message's."""

# The run, in the order the events happened: (event, process, kind, message)
RUN = [
    ("a1", "P1", "local", None),
    ("c1", "P3", "local", None),
    ("a2", "P1", "send", "m1"),
    ("b1", "P2", "recv", "m1"),
    ("b2", "P2", "send", "m2"),
    ("c2", "P3", "recv", "m2"),
    ("b3", "P2", "local", None),
    ("b4", "P2", "send", "m3"),
    ("a3", "P1", "recv", "m3"),
    ("a4", "P1", "send", "m4"),
    ("c3", "P3", "recv", "m4"),
]


def lamport(run):
    clock, stamp, carried = {}, {}, {}
    for e, p, kind, m in run:
        c = clock.get(p, 0)
        if kind == "recv":
            c = max(c, carried[m])
        clock[p] = stamp[e] = c + 1
        if kind == "send":
            carried[m] = stamp[e]
    return stamp


def happened_before(run):
    """The pairs (e, f) with e -> f: process order, send before receive, closed."""
    hb, last, sent = set(), {}, {}
    for e, p, kind, m in run:
        direct = [last[p]] if p in last else []
        if kind == "recv":
            direct.append(sent[m])
        for d in direct:
            hb |= {(d, e)} | {(x, e) for (x, y) in hb if y == d}
        last[p] = e
        if kind == "send":
            sent[m] = e
    return hb


if __name__ == "__main__":
    L, hb = lamport(RUN), happened_before(RUN)
    for p in ("P1", "P2", "P3"):
        print(p, "  ".join(f"{e}:{L[e]}" for e, q, _, _ in RUN if q == p))
    events = [e for e, *_ in RUN]
    ok = all(L[e] < L[f] for e, f in hb)
    print(f"{len(hb)} pairs e -> f, and L(e) < L(f) for all of them: {ok}")
    unrelated = [
        (e, f) for e in events for f in events if L[e] < L[f] and (e, f) not in hb
    ]
    print(
        f"{len(unrelated)} pairs have L(e) < L(f) without e -> f, such as",
        ", ".join(f"{e}:{L[e]} {f}:{L[f]}" for e, f in unrelated[:3]),
    )
