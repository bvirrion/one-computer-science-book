"""brent.py -- a greedy scheduler on p processors: at each time step it runs any
min(p, ready) ready unit-time nodes. On a random DAG and on the merge sort DAG of
workspan.py, its time T_p is compared with the lower bound max(W/p, S) and with
Brent's bound W/p + S."""

import random
from math import ceil

from workspan import merge_sort, work_span


def greedy(preds, p):
    """Steps taken by a greedy schedule, ready nodes taken oldest first."""
    waiting = {v: len(us) for v, us in preds.items()}
    users = {v: [] for v in preds}
    for v, us in preds.items():
        for u in us:
            users[u].append(v)
    ready = [v for v, k in waiting.items() if k == 0]
    steps = 0
    while ready:
        run, ready = ready[:p], ready[p:]
        for u in run:
            for v in users[u]:
                waiting[v] -= 1
                if waiting[v] == 0:
                    ready.append(v)
        steps += 1
    return steps


def random_dag(n, width, seed):
    """n nodes in layers of random width, each using 1 to 3 nodes of earlier layers."""
    rng = random.Random(seed)
    preds, layers = {}, [[]]
    while len(preds) < n:
        layer = list(range(len(preds), min(n, len(preds) + rng.randint(1, width))))
        for v in layer:
            earlier = [u for lay in layers[-3:] for u in lay]
            preds[v] = rng.sample(earlier, min(len(earlier), rng.randint(1, 3)))
        layers.append(layer)
    return preds


if __name__ == "__main__":
    for name, dag in (
        ("random DAG", random_dag(2000, 12, 24)),
        ("merge sort of 256", merge_sort(256)[0]),
    ):
        w, s = work_span(dag)
        print(f"{name}: work W = {w}, span S = {s}")
        print(" p    T_p  max(W/p, S)  W/p + S  T_p / lower bound")
        for p in range(1, 9):
            t, low = greedy(dag, p), max(ceil(w / p), s)
            print(f"{p:>2} {t:>6} {low:>12} {w / p + s:>8.0f} {t / low:>18.2f}")
