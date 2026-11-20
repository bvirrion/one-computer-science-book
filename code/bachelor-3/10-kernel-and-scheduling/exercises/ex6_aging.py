"""ex6_aging.py -- priority scheduling with aging: a lower number runs first, and a
job's priority improves by one for every `age` units it waits, so no job waits for
ever. Non-preemptive; ties go to the earliest arrival."""


def priority_run(jobs, prio, age):
    """jobs: (name, arrival, burst); prio: name -> base priority.
    Returns name -> finish time."""
    pending = sorted(jobs, key=lambda j: j[1])
    ready, finish, t = [], {}, 0
    while pending or ready:
        while pending and pending[0][1] <= t:
            ready.append(pending.pop(0))
        if not ready:
            t = pending[0][1]
            continue
        job = min(ready, key=lambda j: (prio[j[0]] - (t - j[1]) // age, j[1]))
        ready.remove(job)
        t += job[2]
        finish[job[0]] = t
    return finish
