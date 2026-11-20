"""One room, many requests: keep as many bookings as possible, earliest end first."""
import random

rng = random.Random(11)
requests = []
for name in "ABCDEFGHIJKL":
    start = rng.randint(8, 18)
    requests.append((name, start, start + rng.randint(1, 3)))   # hours, end excluded


def earliest_end_first(requests):
    chosen, free_from = [], 0
    for name, start, end in sorted(requests, key=lambda r: r[2]):
        if start >= free_from:            # does not overlap the last one kept
            chosen.append((name, start, end))
            free_from = end
    return chosen


for name, start, end in sorted(requests, key=lambda r: r[2]):
    print(f"{name}: {start:2}h-{end:2}h")
print("kept:", " ".join(name for name, _, _ in earliest_end_first(requests)))
