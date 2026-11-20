"""disk_sched.py -- the order in which three disk schedulers serve one queue of
requests, and how far the head travels, in cylinders."""
import random

CYLINDERS = 200


def fcfs(head, queue):
    return list(queue)


def sstf(head, queue):  # shortest seek time first: always the nearest request
    left, order = list(queue), []
    while left:
        head = min(left, key=lambda c: abs(c - head))
        left.remove(head)
        order.append(head)
    return order


def scan(head, queue, up=True):  # the elevator: sweep to the end, then turn back
    above = sorted(c for c in queue if c >= head)
    below = sorted((c for c in queue if c < head), reverse=True)
    return above + below if up else below + above


def travel(head, order, policy):
    if policy is scan and order and min(order) < head:  # up to the last cylinder first
        return (CYLINDERS - 1 - head) + (CYLINDERS - 1 - min(order))
    return sum(abs(b - a) for a, b in zip([head] + order, order))


if __name__ == "__main__":
    rng = random.Random(12)
    queue = [rng.randrange(CYLINDERS) for _ in range(10)]
    head = 100
    print(f"head at {head}, moving up; queue {queue}")
    for name, policy in (("FCFS", fcfs), ("SSTF", sstf), ("SCAN", scan)):
        order = policy(head, queue)
        moves = travel(head, order, policy)
        print(f"{name}: {' '.join(map(str, order))}   travel {moves}")
