"""sched.py -- a CPU scheduling simulator. Jobs arrive with a burst of work; a policy
picks the next job from the ready queue; a switch from one job to another costs
`switch` units."""
from dataclasses import dataclass, field


@dataclass
class Job:
    name: str
    arrival: int
    burst: int


@dataclass
class Result:
    gantt: list = field(default_factory=list)  # (start, end, name); "*" is a switch
    finish: dict = field(default_factory=dict)
    first: dict = field(default_factory=dict)  # when each job first ran

    def averages(self, jobs):
        n = len(jobs)
        turn = sum(self.finish[j.name] - j.arrival for j in jobs) / n
        wait = sum(self.finish[j.name] - j.arrival - j.burst for j in jobs) / n
        resp = sum(self.first[j.name] - j.arrival for j in jobs) / n
        return turn, wait, resp


def fifo(ready, left):
    return ready.pop(0)


def shortest(ready, left):  # the least work left; ties to the earliest in the queue
    j = min(ready, key=lambda name: left[name])
    ready.remove(j)
    return j


def simulate(jobs, pick=fifo, quantum=None, preempt=False, switch=0):
    """quantum: at most that long per turn (round robin);
    preempt: stop at every arrival."""
    pending = sorted(jobs, key=lambda j: j.arrival)
    left = {j.name: j.burst for j in jobs}
    ready, r, t, last = [], Result(), 0, None

    def admit(now):
        while pending and pending[0].arrival <= now:
            ready.append(pending.pop(0).name)

    while pending or ready:
        admit(t)
        if not ready:
            t = pending[0].arrival
            continue
        j = pick(ready, left)
        if last is not None and last != j and switch:
            r.gantt.append((t, t + switch, "*"))
            t += switch
            admit(t)
        r.first.setdefault(j, t)
        run = left[j] if quantum is None else min(quantum, left[j])
        if preempt and pending:
            run = min(run, max(pending[0].arrival - t, 1))
        if r.gantt and r.gantt[-1][2] == j and r.gantt[-1][1] == t:
            r.gantt[-1] = (r.gantt[-1][0], t + run, j)  # the same job goes on
        else:
            r.gantt.append((t, t + run, j))
        t += run
        left[j] -= run
        admit(t)  # arrivals during the turn queue before the job that ran
        if left[j] == 0:
            r.finish[j] = t
        else:
            ready.append(j)
        last = j
    return r


def gantt_row(r):
    return " ".join(f"{name}[{a},{b})" for a, b, name in r.gantt)
