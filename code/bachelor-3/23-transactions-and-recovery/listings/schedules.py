"""schedules.py -- conflict serialisability. A schedule is a list of operations
(transaction, action, item), action R or W. Two operations conflict when they
belong to different transactions, touch the same item and one of them writes."""

from itertools import combinations


def parse(text):
    """'R1(A) W2(A)' -> [(1, 'R', 'A'), (2, 'W', 'A')]"""
    return [
        (int(op[1 : op.index("(")]), op[0], op[op.index("(") + 1 : -1])
        for op in text.split()
    ]


def conflict(p, q):
    return p[0] != q[0] and p[2] == q[2] and "W" in (p[1], q[1])


def precedence_graph(schedule):
    """An edge Ti -> Tj for each conflict in which Ti's operation comes first."""
    edges = set()
    for i, j in combinations(range(len(schedule)), 2):
        if conflict(schedule[i], schedule[j]):
            edges.add((schedule[i][0], schedule[j][0]))
    return edges


def serial_order(schedule):
    """A serial order of the transactions with the same conflicts (a topological
    order of the graph), or None if the graph has a cycle."""
    nodes = sorted({op[0] for op in schedule})
    edges = precedence_graph(schedule)
    order = []
    while nodes:
        free = [n for n in nodes if not any(b == n and a in nodes for a, b in edges)]
        if not free:
            return None  # every remaining transaction has a predecessor: a cycle
        order.append(free[0])
        nodes.remove(free[0])
    return order


def interleavings(t1, t2):
    """Every schedule that keeps the order of t1's and of t2's operations."""
    n = len(t1) + len(t2)
    for slots in combinations(range(n), len(t1)):
        a, b, out = iter(t1), iter(t2), []
        for k in range(n):
            out.append(next(a) if k in slots else next(b))
        yield out


SCHEDULES = {
    "serial": "R1(A) W1(A) R1(B) W1(B) R2(A) W2(A) R2(B) W2(B)",
    "interleaved": "R1(A) W1(A) R2(A) W2(A) R1(B) W1(B) R2(B) W2(B)",
    "lost update": "R1(A) R2(A) W1(A) W2(A)",
    "crossed": "R1(A) W1(A) R2(A) W2(A) R2(B) W2(B) R1(B) W1(B)",
    "three": "R1(A) W2(A) R2(B) W3(B) R3(C) W1(C)",
    "blind writes": "W1(A) W2(A) W2(B) W1(B) W3(A) W3(B)",
}

if __name__ == "__main__":
    for name, text in SCHEDULES.items():
        s = parse(text)
        edges = " ".join(f"T{a}->T{b}" for a, b in sorted(precedence_graph(s)))
        order = serial_order(s)
        verdict = " ".join(f"T{t}" for t in order) if order else "not serialisable"
        print(f"{name:<13} {edges:<20} {verdict}")
    t1 = parse("R1(A) W1(A) R1(B) W1(B)")
    t2 = parse("R2(A) W2(A) R2(B) W2(B)")
    all_s = list(interleavings(t1, t2))
    ok = sum(serial_order(s) is not None for s in all_s)
    print(f"{len(all_s)} interleavings of two 4-step transactions: {ok} serialisable")
