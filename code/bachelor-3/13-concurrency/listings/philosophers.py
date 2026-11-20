"""philosophers.py -- every interleaving of n dining philosophers, explored as a graph
of states: how many states are reachable, and which of them are deadlocked."""
from collections import deque

THINK, HOLD1, EAT = 0, 1, 2  # where each philosopher is in its loop


def forks(i, n, ordered):  # which fork philosopher i takes first, and second
    left, right = i, (i + 1) % n
    return (min(left, right), max(left, right)) if ordered else (left, right)


def moves(state, n, ordered):
    """Every step one philosopher can take: (philosopher, next state)."""
    pcs, owner = state
    for i, pc in enumerate(pcs):
        first, second = forks(i, n, ordered)
        if pc == THINK and owner[first] is None:  # take the first fork
            yield i, step(state, i, HOLD1, {first: i})
        elif pc == HOLD1 and owner[second] is None:  # take the second: eat
            yield i, step(state, i, EAT, {second: i})
        elif pc == EAT:  # put both down
            yield i, step(state, i, THINK, {first: None, second: None})


def step(state, i, pc, changes):
    pcs, owner = state
    pcs, owner = list(pcs), list(owner)
    pcs[i] = pc
    for f, who in changes.items():
        owner[f] = who
    return tuple(pcs), tuple(owner)


def explore(n, ordered=False):
    start = ((THINK,) * n, (None,) * n)
    seen, todo, dead = {start}, deque([start]), []
    while todo:
        state = todo.popleft()
        nexts = [s for _, s in moves(state, n, ordered)]
        if not nexts:
            dead.append(state)
        for s in nexts:
            if s not in seen:
                seen.add(s)
                todo.append(s)
    return seen, dead


if __name__ == "__main__":
    print(" n   naive: states deadlocked   ordered: states deadlocked")
    for n in range(2, 8):
        (s1, d1), (s2, d2) = explore(n), explore(n, ordered=True)
        print(f"{n:>2}   {len(s1):>13} {len(d1):>10}   {len(s2):>15} {len(d2):>10}")
    _, dead = explore(5)
    print("the deadlocked state for n = 5:", dead[0])
