from scheduler import fcfs, gantt, round_robin, times

workload = [("A", 0, 5), ("B", 1, 3), ("C", 2, 8), ("D", 3, 2)]   # name, arrival, burst
for title, slices in [("FCFS     ", fcfs(workload)),
                      ("RR, q = 2", round_robin(workload, 2)),
                      ("RR, q = 4", round_robin(workload, 4))]:
    t = times(workload, slices)
    mean_turn = sum(a for a, _ in t.values()) / len(t)
    mean_wait = sum(w for _, w in t.values()) / len(t)
    first = {}
    for name, start, _ in slices:
        first.setdefault(name, start)            # the first time each one runs
    response = sum(first[n] - a for n, a, _ in workload) / len(workload)
    print(f"{title}  {gantt(slices)}")
    print(f"           turnaround {mean_turn:5.2f}   waiting {mean_wait:5.2f}"
          f"   response {response:4.2f}   {len(slices)} slices")
