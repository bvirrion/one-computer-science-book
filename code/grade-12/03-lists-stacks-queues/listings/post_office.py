"""A day at the post office: 480 minutes of arrivals, one clerk, two queues."""
import random

import queue_linked
import queue_two_stacks


def simulate(Queue, seed=2026):
    rng = random.Random(seed)
    line = Queue()
    waiting = longest_line = longest_wait = customers = 0
    busy_until = 0
    minute = 0
    while minute < 480 or not line.is_empty():   # doors close, the line is served
        if minute < 480 and rng.random() < 0.3:      # an arrival this minute
            line.enqueue(minute)
            customers += 1
            waiting += 1
        if minute >= busy_until and not line.is_empty():
            arrived = line.dequeue()
            waiting -= 1
            longest_wait = max(longest_wait, minute - arrived)
            busy_until = minute + rng.randint(1, 5)  # service of 1 to 5 minutes
        longest_line = max(longest_line, waiting)
        minute += 1
    return customers, longest_line, longest_wait, line.moves


for module in [queue_linked, queue_two_stacks]:
    customers, length, wait, moves = simulate(module.Queue)
    print(f"{module.__name__}: {customers} customers, longest line {length},"
          f" longest wait {wait} min")
    print(f"  moves {moves} = {moves / customers:.2f} per customer")
