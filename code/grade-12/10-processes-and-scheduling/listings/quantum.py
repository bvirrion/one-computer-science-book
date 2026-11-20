"""Choosing the quantum: mean turnaround of round robin, with a context switch of 1."""
from scheduler import fcfs, round_robin, times

workload = [("A", 0, 20), ("B", 1, 3), ("C", 2, 6), ("D", 3, 2), ("E", 5, 4)]
SWITCH = 1


def mean_turnaround(slices):
    t = times(workload, slices)
    return sum(turn for turn, _ in t.values()) / len(t)


def switches(slices):
    return sum(a[0] != b[0] for a, b in zip(slices, slices[1:]))


slices = fcfs(workload, SWITCH)
print(f"FCFS   : mean turnaround {mean_turnaround(slices):5.1f}, "
      f"{switches(slices):2} switches, all done at {slices[-1][2]}")
best = None
for q in range(1, 13):
    slices = round_robin(workload, q, SWITCH)
    m = mean_turnaround(slices)
    print(f"q = {q:2} : mean turnaround {m:5.1f}, {switches(slices):2} switches,"
          f" all done at {slices[-1][2]}")
    if best is None or m < best[1]:
        best = (q, m)
print("best quantum:", best[0], "with a mean turnaround of", best[1])
