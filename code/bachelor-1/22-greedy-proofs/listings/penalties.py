"""penalties.py: unit tasks on one machine, each with a deadline and a penalty if late:
the greedy schedule by decreasing penalty, against all subsets."""

import random
from itertools import combinations


def feasible(tasks):
    """Can all these tasks be on time? Iff at most t of them have a deadline <= t."""
    deadlines = sorted(d for d, _ in tasks)
    return all(d >= i + 1 for i, d in enumerate(deadlines))


def greedy(tasks):
    """On-time tasks: by decreasing penalty, keep a task if the set stays feasible."""
    on_time = []
    for task in sorted(tasks, key=lambda t: -t[1]):
        if feasible(on_time + [task]):
            on_time.append(task)
    return on_time


def schedule(on_time, tasks):
    """On-time tasks by increasing deadline, then the late ones in any order."""
    late = list(tasks)
    for t in on_time:
        late.remove(t)
    return sorted(on_time) + late


def best_penalty(tasks):
    """The smallest total penalty, by trying every set of on-time tasks."""
    total = sum(p for _, p in tasks)
    return min(total - sum(p for _, p in s) for k in range(len(tasks) + 1)
               for s in combinations(tasks, k) if feasible(list(s)))


def main():
    # (deadline, penalty)
    tasks = [(2, 45), (1, 25), (3, 60), (2, 35), (4, 15), (3, 50), (4, 10)]
    on_time = greedy(tasks)
    for slot, task in enumerate(schedule(on_time, tasks), start=1):
        print(f"slot {slot}: deadline {task[0]}, penalty {task[1]:2}",
              "on time" if task in on_time else "late")
    total = sum(p for _, p in tasks) - sum(p for _, p in on_time)
    print("total penalty", total, "- smallest possible", best_penalty(tasks))
    rng = random.Random(22)
    agree = 0
    for _ in range(300):
        n = rng.randint(1, 9)
        tasks = [(rng.randint(1, 6), rng.randint(1, 50)) for _ in range(n)]
        paid = sum(p for _, p in tasks) - sum(p for _, p in greedy(tasks))
        agree += paid == best_penalty(tasks)
    print(f"greedy optimal on {agree} of 300 random sets")


if __name__ == "__main__":
    main()
