"""Exercises of the chapter on processes and scheduling."""
import sys
from collections import deque
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "listings"))
from scheduler import times  # noqa: E402


def turnaround(workload, slices):                  # exercise 5
    finish = {name: end for name, _, end in slices}
    return {name: finish[name] - arrival for name, arrival, _ in workload}


def round_robin_no_requeue(workload, quantum):     # exercise 6: the staged fault
    waiting, ready, time, slices = deque(workload), deque(), 0, []
    left = {name: burst for name, _, burst in workload}
    while waiting or ready:
        while waiting and waiting[0][1] <= time:
            ready.append(waiting.popleft()[0])
        if not ready:
            time = waiting[0][1]
            continue
        name = ready.popleft()
        run = min(quantum, left[name])
        slices.append((name, time, time + run))
        time += run
        left[name] -= run                          # never put back in the queue
    return slices, left


def count_interleavings(a, b):                     # exercise 7
    return sum(1 for _ in combinations(range(a + b), a))


def sjf(workload):                                 # exercise 8: shortest job first
    pending, time, slices = sorted(workload, key=lambda w: w[1]), 0, []
    while pending:
        arrived = [w for w in pending if w[1] <= time]
        if not arrived:
            time = pending[0][1]
            continue
        job = min(arrived, key=lambda w: (w[2], w[1]))
        pending.remove(job)
        slices.append((job[0], time, time + job[2]))
        time += job[2]
    return slices


def has_cycle(waits_for):                          # exercise 13
    """waits_for: process -> the processes it waits for. Is there a cycle?"""
    state = {}

    def visit(v):
        state[v] = "open"
        for w in waits_for.get(v, []):
            if state.get(w) == "open" or (w not in state and visit(w)):
                return True
        state[v] = "done"
        return False

    return any(v not in state and visit(v) for v in list(waits_for))


def philosophers(n, ordered):                      # exercise 15
    """n philosophers, n forks; each takes two forks. Is a deadlock reachable?"""
    def forks(k):
        a, b = k, (k + 1) % n
        return (min(a, b), max(a, b)) if ordered else (a, b)

    seen = set()

    def go(holding):                               # holding: forks held by each
        if holding in seen:
            return False
        seen.add(holding)
        owner = {f: k for k, fs in enumerate(holding) for f in fs}
        moves = []
        for k in range(n):
            if len(holding[k]) == 2:
                moves.append(holding[:k] + ((),) + holding[k + 1:])   # eats, frees both
            else:
                f = forks(k)[len(holding[k])]
                if f not in owner:
                    moves.append(holding[:k] + (holding[k] + (f,),) + holding[k + 1:])
        if not moves:
            return True                            # nobody can move: deadlock
        return any(go(m) for m in moves)

    return go(((),) * n)


if __name__ == "__main__":
    w = [("A", 0, 5), ("B", 1, 3), ("C", 2, 8), ("D", 3, 2)]
    print(turnaround(w, sjf(w)), times(w, sjf(w)))
    print(round_robin_no_requeue(w, 2))
    print(count_interleavings(3, 3), has_cycle({"P": ["Q"], "Q": ["P"]}))
    print(philosophers(5, False), philosophers(5, True))
