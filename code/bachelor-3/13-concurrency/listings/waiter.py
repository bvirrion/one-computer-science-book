"""waiter.py -- the waiter's fix: a hungry philosopher eats only when the waiter, a
monitor, can hand it both forks at once. No deadlock; but can a philosopher starve?"""
from collections import deque

THINK, HUNGRY, EAT = 0, 1, 2


def can_eat(pcs, i, n):  # both neighbours are not eating: both forks are free
    return pcs[(i - 1) % n] != EAT and pcs[(i + 1) % n] != EAT


def moves(pcs, n):
    for i, pc in enumerate(pcs):
        if pc == THINK:
            yield i, pcs[:i] + (HUNGRY,) + pcs[i + 1:]
        elif pc == HUNGRY and can_eat(pcs, i, n):
            yield i, pcs[:i] + (EAT,) + pcs[i + 1:]
        elif pc == EAT:
            yield i, pcs[:i] + (THINK,) + pcs[i + 1:]


def explore(n):
    start = (THINK,) * n
    seen, todo, dead = {start}, deque([start]), 0
    while todo:
        pcs = todo.popleft()
        nexts = [s for _, s in moves(pcs, n)]
        dead += not nexts
        for s in nexts:
            if s not in seen:
                seen.add(s)
                todo.append(s)
    return seen, dead


def starving_cycle(n, victim=0):
    """A closed walk through reachable states in which the victim stays hungry and never
    has both forks free, while every other philosopher moves: it starves alone."""
    def blocked(pcs):
        return pcs[victim] == HUNGRY and not can_eat(pcs, victim, n)

    nodes = sorted(p for p in explore(n)[0] if blocked(p))
    edges = {p: [(i, q) for i, q in moves(p, n) if i != victim and blocked(q)]
             for p in nodes}

    def path(a, b):  # shortest walk from a to b inside the blocked states
        prev, todo = {a: None}, deque([a])
        while todo:
            p = todo.popleft()
            for i, q in edges[p]:
                if q not in prev:
                    prev[q] = (p, i)
                    todo.append(q)
        if b not in prev:
            return None
        walk = []
        while b != a:
            p, i = prev[b]
            walk.append((i, b))
            b = p
        return walk[::-1]

    for start in nodes:  # a start from which each other philosopher can move and return
        walk, here = [], start
        for j in range(n):
            if j == victim:
                continue
            move = next(((p, i, q) for p in nodes for i, q in edges[p] if i == j
                         and path(here, p) is not None and path(q, start) is not None),
                        None)
            if move is None:
                break
            p, i, q = move
            walk += path(here, p) + [(i, q)]
            here = q
        else:
            return walk + path(here, start)
    return None


if __name__ == "__main__":
    for n in range(3, 8):
        states, dead = explore(n)
        print(f"n = {n}: {len(states)} states, {dead} deadlocked")
    names = "THE"  # thinking, hungry, eating
    cycle = starving_cycle(5)
    print("a schedule that starves philosopher 0 (T thinks, H hungry, E eats):")
    print(f"  from                 {' '.join(names[p] for p in cycle[-1][1])}")
    for i, pcs in cycle:
        print(f"  philosopher {i} moves: {' '.join(names[p] for p in pcs)}")
