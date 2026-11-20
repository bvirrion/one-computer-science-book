"""counter.py: a 3-bit synchronous counter (every flip-flop on the same clock, next
state from gates) and a ripple counter (each flip-flop clocked by the one before),
watched at every time unit while they settle; each flip-flop takes d units."""


def synchronous_next(q):
    """q = (q0, q1, q2), q0 the low bit: add 1 with gates."""
    q0, q1, q2 = q
    return (1 - q0, q1 ^ q0, q2 ^ (q1 & q0))


def synchronous(cycles, d=2):
    """The value seen at each time unit; the clock rises every 10 units."""
    q, seen = (0, 0, 0), []
    for t in range(10 * cycles):
        if t % 10 == d:  # every flip-flop changes d units after the shared edge
            q = synchronous_next(q)
        seen.append(q[0] + 2 * q[1] + 4 * q[2])
    return seen


def ripple(cycles, d=2, n=3):
    """Flip-flop i toggles d units after flip-flop i - 1 falls from 1 to 0."""
    q, seen, changes = [0] * n, [], {}  # changes: time -> the flip-flops to toggle
    for t in range(10 * cycles):
        if t % 10 == 0:
            changes.setdefault(t + d, []).append(0)
        for i in changes.pop(t, []):
            q[i] ^= 1
            if q[i] == 0 and i + 1 < n:  # it fell: the next one toggles d later
                changes.setdefault(t + d, []).append(i + 1)
        seen.append(sum(b << i for i, b in enumerate(q)))
    return seen


def settling(seen):
    """The most time units after a clock edge before the value stops changing."""
    return max(max((u for u in range(1, 10) if seen[c + u] != seen[c + u - 1]),
                   default=0) for c in range(0, len(seen), 10))


def values_between_edges(seen):
    """Group the values seen by clock cycle, dropping repeats."""
    cycles = []
    for c in range(len(seen) // 10):
        run = [seen[10 * c]]
        for v in seen[10 * c + 1:10 * c + 10]:
            if v != run[-1]:
                run.append(v)
        cycles.append(run)
    return cycles


if __name__ == "__main__":
    for name, counter in [("synchronous", synchronous), ("ripple", ripple)]:
        cycles = values_between_edges(counter(8))
        glitches = sum(len(run) - 2 for run in cycles)
        print(f"{name:11}", " | ".join(" ".join(map(str, run)) for run in cycles))
        print(f"{'':11} values that are neither the old count nor the new: {glitches}")
    for n in (3, 4):
        seen = ripple(2 ** n, n=n)
        print(f"ripple, {n} bits: settled {settling(seen)} units after the edge; "
              f"synchronous: {settling(synchronous(8))}")
