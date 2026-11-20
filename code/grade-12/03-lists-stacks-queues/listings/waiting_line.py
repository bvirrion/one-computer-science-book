"""Ten minutes at a counter: one person served per two minutes."""
import random

from queue_linked import Queue

rng = random.Random(7)
line, served = Queue(), 0
for minute in range(10):
    arrived = [f"c{minute}{k}" for k in range(rng.randint(0, 2))]
    for person in arrived:
        line.enqueue(person)
    leaving = line.dequeue() if minute % 2 == 1 and not line.is_empty() else "-"
    print(f"minute {minute}: arrive {' '.join(arrived) or '-':8} served {leaving}")
