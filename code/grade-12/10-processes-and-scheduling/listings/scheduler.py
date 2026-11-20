"""Two schedulers, simulated: first come first served, and round robin."""
from collections import deque


def fcfs(workload, switch=0):
    """workload: (name, arrival, burst) by arrival. Return slices (name, start, end)."""
    time, slices = 0, []
    for name, arrival, burst in workload:
        if slices and time >= arrival:
            time += switch                       # switching to the next process
        time = max(time, arrival)
        slices.append((name, time, time + burst))
        time += burst
    return slices


def round_robin(workload, quantum, switch=0):
    left = {name: burst for name, _, burst in workload}
    waiting = deque(workload)                    # not yet arrived, by arrival
    ready, time, slices, last = deque(), 0, [], None
    while waiting or ready:
        while waiting and waiting[0][1] <= time:
            ready.append(waiting.popleft()[0])   # arrivals join the end of the queue
        if not ready:
            time = waiting[0][1]                 # the processor is idle until then
            continue
        name = ready.popleft()
        if last is not None and last != name:
            time += switch                       # a context switch
        run = min(quantum, left[name])
        slices.append((name, time, time + run))
        time += run
        left[name] -= run
        while waiting and waiting[0][1] <= time:
            ready.append(waiting.popleft()[0])
        if left[name] > 0:
            ready.append(name)                   # back to the end of the queue
        last = name
    return slices


def times(workload, slices):
    """Turnaround (finish - arrival) and waiting (turnaround - burst) of each."""
    finish = {name: end for name, _, end in slices}
    return {name: (finish[name] - arrival, finish[name] - arrival - burst)
            for name, arrival, burst in workload}


def gantt(slices):
    """One line of text: one letter per time unit, '.' when no process runs."""
    line, time = "", 0
    for name, start, end in slices:
        line += "." * (start - time)             # idle, or switching
        line += name * (end - start)
        time = end
    return line
