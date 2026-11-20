"""partition_rooms.py: all the talks, in as few rooms as possible."""

import heapq
import random

from intervals import random_talks


def max_overlap(talks):
    """The largest number of talks going on at one moment."""
    events = sorted([(s, 1) for s, _ in talks] + [(e, -1) for _, e in talks])
    now = best = 0
    for _, change in events:  # at equal times, ends (-1) come before starts (+1)
        now += change
        best = max(best, now)
    return best


def rooms(talks):
    """Rooms by increasing start: reuse a room whose last talk is over, if any."""
    free_at = []  # heap of (end of the room's last talk, room number)
    assignment, opened = {}, 0
    for talk in sorted(talks):
        if free_at and free_at[0][0] <= talk[0]:
            _, room = heapq.heappop(free_at)  # the room that frees up first
        else:
            room, opened = opened, opened + 1  # every room is busy: open a new one
        assignment[talk] = room
        heapq.heappush(free_at, (talk[1], room))
    return assignment


def main():
    rng = random.Random(22)
    talks = random_talks(rng, 40)
    assignment = rooms(talks)
    used = len(set(assignment.values()))
    print(f"40 talks: maximum overlap {max_overlap(talks)}, rooms used {used}")
    for room in range(used):
        print(f"  room {room}:", sorted(t for t in assignment if assignment[t] == room))


if __name__ == "__main__":
    main()
