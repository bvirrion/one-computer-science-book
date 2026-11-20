"""fcfs_sjf.py -- five jobs under first come first served, shortest job first, shortest
remaining time first and round robin: the timeline and the three averages."""
from sched import Job, fifo, gantt_row, shortest, simulate

jobs = [Job("A", 0, 8), Job("B", 1, 4), Job("C", 2, 9), Job("D", 3, 5), Job("E", 6, 2)]
runs = {
    "FCFS": simulate(jobs, fifo),
    "SJF": simulate(jobs, shortest),
    "SRTF": simulate(jobs, shortest, preempt=True),
    "RR q=3": simulate(jobs, fifo, quantum=3),
}
print(f"{'policy':<7} {'turnaround':>10} {'waiting':>8} {'response':>9}")
for name, r in runs.items():
    turn, wait, resp = r.averages(jobs)
    print(f"{name:<7} {turn:>10.1f} {wait:>8.1f} {resp:>9.1f}")
for name, r in runs.items():
    print(f"{name}: {gantt_row(r)}")
