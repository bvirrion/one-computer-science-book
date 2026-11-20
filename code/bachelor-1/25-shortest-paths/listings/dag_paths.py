"""dag_paths.py: the critical path of a project, a longest path in a directed acyclic
graph, by relaxing the arcs in topological order."""

TASKS = {  # task: (days, tasks that must be finished first)
    "design": (3, []),
    "database": (5, ["design"]),
    "interface": (4, ["design"]),
    "import": (2, ["database"]),
    "tests": (3, ["database", "interface"]),
    "manual": (2, ["interface"]),
    "training": (1, ["manual", "tests"]),
    "launch": (1, ["import", "tests", "training"]),
}


def topological(tasks):
    order, done = [], set()

    def visit(t):
        done.add(t)
        for before in tasks[t][1]:
            if before not in done:
                visit(before)
        order.append(t)  # after everything it depends on

    for t in tasks:
        if t not in done:
            visit(t)
    return order


def critical_path(tasks):
    """(start, length, path): start[t] is the earliest day t can start."""
    start, via = {}, {}
    for t in topological(tasks):
        start[t], via[t] = 0, None
        for before in tasks[t][1]:  # relax the arc before -> t, keeping the maximum
            end = start[before] + tasks[before][0]
            if end > start[t]:
                start[t], via[t] = end, before
    last = max(tasks, key=lambda t: start[t] + tasks[t][0])
    path = [last]
    while via[path[-1]] is not None:
        path.append(via[path[-1]])
    return start, start[last] + tasks[last][0], path[::-1]


if __name__ == "__main__":
    start, length, path = critical_path(TASKS)
    days = [f"{t} {d}" for t, d in start.items()]
    print("earliest start:", ", ".join(days[:4]) + ",\n  " + ", ".join(days[4:]))
    print(f"project: {length} days; critical path:", " > ".join(path))
