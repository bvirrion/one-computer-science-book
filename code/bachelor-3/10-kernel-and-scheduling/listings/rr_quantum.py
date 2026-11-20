"""rr_quantum.py -- the weekend problem: the print shop's jobs under round robin with a
switch cost of s = 1, for quanta 1 to 20, against first come first served and
shortest job first, which pay the same switch cost from one job to the next."""
import random

from sched import Job, fifo, shortest, simulate

rng = random.Random(2026)
jobs, t = [], 0
for k in range(60):  # one job every 45 units on average; one in five is long
    t += round(rng.expovariate(1 / 45))
    burst = rng.randint(2, 12) if rng.random() < 0.8 else rng.randint(40, 120)
    jobs.append(Job(f"J{k}", t, burst))
work = sum(j.burst for j in jobs)
load = work / jobs[-1].arrival
print(f"{len(jobs)} jobs, {work} units of work, last arrival {jobs[-1].arrival},"
      f" load {load:.2f}")
for name, pick in (("FCFS", fifo), ("SJF", shortest)):
    turn, _, resp = simulate(jobs, pick, switch=1).averages(jobs)
    print(f"{name:<4}  turnaround {turn:6.1f}  response {resp:5.1f}")
head = f"{'turnaround':>10} {'response':>8} {'switches':>8}"
head += f" {'overhead':>8} {'s/(q+s)':>7}"
print(f"{'q':>3} {head} {'load(q+s)/q':>11}")
for q in range(1, 21):
    r = simulate(jobs, fifo, quantum=q, switch=1)
    turn, _, resp = r.averages(jobs)
    n = sum(1 for _, _, name in r.gantt if name == "*")
    print(f"{q:>3} {turn:>10.1f} {resp:>8.1f} {n:>8} {n / (n + work):>8.3f}"
          f" {1 / (q + 1):>7.3f} {load * (q + 1) / q:>11.2f}")
