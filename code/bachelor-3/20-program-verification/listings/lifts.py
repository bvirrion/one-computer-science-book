"""lifts.py -- n lifts share one shaft section, guarded by a lock. Each lift goes
idle -> waiting -> in the shaft -> idle. In the correct protocol, taking the lock is
one atomic step; in the buggy one, a lift tests the lock, then takes it in a second
step."""

import math
from collections import deque

IDLE, WAIT, READY, SHAFT = "I", "W", "R", "S"


def moves(state, atomic):
    """Every state reachable in one step of one lift. A state is (lock, positions)."""
    lock, pos = state
    for i, p in enumerate(pos):

        def at(q, new_lock=lock, i=i):
            return new_lock, pos[:i] + (q,) + pos[i + 1 :]

        if p == IDLE:
            yield i, at(WAIT)
        elif p == WAIT and lock == 0:  # the lock is free
            yield i, at(SHAFT, 1) if atomic else at(READY)
        elif p == READY:  # buggy: takes the lock without testing again
            yield i, at(SHAFT, 1)
        elif p == SHAFT:
            yield i, at(IDLE, 0)


def check(n, atomic):
    start = (0, (IDLE,) * n)
    depth, queue = {start: 0}, deque([start])
    while queue:
        s = queue.popleft()
        if s[1].count(SHAFT) > 1:
            return len(depth), depth[s]  # mutual exclusion fails after depth[s] steps
        for _, t in moves(s, atomic):
            if t not in depth:
                depth[t] = depth[s] + 1
                queue.append(t)
    return len(depth), None


if __name__ == "__main__":
    print("lifts   states   buggy: fails after")
    sizes = []
    for n in range(1, 7):
        states, bad = check(n, atomic=True)
        assert bad is None  # AG not two lifts in the shaft
        sizes.append(states)
        bad = check(n, atomic=False)[1]
        print(f"{n:>5} {states:>8}   {f'{bad} steps' if bad else 'never'}")
    # least squares on log(states) = log c + n log b
    xs, ys = range(1, 7), [math.log(s) for s in sizes]
    mx, my = sum(xs) / 6, sum(ys) / 6
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum(
        (x - mx) ** 2 for x in xs
    )
    print(f"fit: states = {math.exp(my - slope * mx):.2f} * {math.exp(slope):.3f}^n")
