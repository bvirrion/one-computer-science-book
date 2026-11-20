"""exo_by_start.py: exercise 5, the interval greedy with the talks sorted by start."""


def scan(talks, key):
    kept = []
    for t in sorted(talks, key=key):
        if not kept or kept[-1][1] <= t[0]:  # starts after the last talk kept ends
            kept.append(t)
    return kept


if __name__ == "__main__":
    talks = [(0, 100), (10, 30), (35, 55), (60, 80), (85, 99)]
    print("by start: ", scan(talks, key=lambda t: t[0]))
    print("by finish:", scan(talks, key=lambda t: t[1]))
