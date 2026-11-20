"""mlfq.py -- a multilevel feedback queue: three levels with quanta 2, 4 and 8. A job
that uses up its quantum moves down a level; one that blocks for input first keeps
its level. A job of a higher level preempts a lower one as soon as it is ready."""
QUANTA = [2, 4, 8]
JOBS = {"render": (0, [40]), "edit": (1, [1] * 8)}  # arrival, CPU bursts
WAIT = 4  # between two bursts, a job waits this long for input

level = {name: 0 for name in JOBS}
bursts = {name: list(b) for name, (_, b) in JOBS.items()}
ready_at = {name: arrival for name, (arrival, _) in JOBS.items()}
queues, trace, waited = [[], [], []], [], []
t, current, used = 0, None, 0
while any(bursts.values()):
    for name in JOBS:  # a job that becomes ready joins the back of its level's queue
        if ready_at[name] is not None and ready_at[name] <= t:
            queues[level[name]].append(name)
            if name == "edit":
                waited.append(-t)  # completed when it runs
            ready_at[name] = None
    if current and any(queues[:level[current]]):  # preempted by a higher level
        queues[level[current]].insert(0, current)
        current = None
    if current is None:
        busy = [q for q in queues if q]
        if not busy:
            t += 1
            continue
        current, used = busy[0].pop(0), 0
        if current == "edit":
            waited[-1] += t
        trace.append([t, t, current, level[current]])
    t, used = t + 1, used + 1
    trace[-1][1] = t
    bursts[current][0] -= 1
    if bursts[current][0] == 0:  # the burst is over: wait for input, keep the level
        bursts[current].pop(0)
        ready_at[current] = t + WAIT if bursts[current] else None
        current = None
    elif used == QUANTA[level[current]]:
        level[current] = min(level[current] + 1, len(QUANTA) - 1)
        queues[level[current]].append(current)
        current = None
for start, end, name, lv in trace[:12]:
    print(f"{start:>3}-{end:<3} {name:<6} level {lv}")
print(f"... {len(trace)} turns in all, the last ends at t = {t}")
print("edit's wait from ready to running:", " ".join(map(str, waited)))
