"""backoff_sim.py: k stations, one frame each, binary exponential backoff."""
import random


def run(k, rng, cap=10):
    """Slots until every frame is through; and the mean slot at which a frame is."""
    wait = [0] * k                            # slots each station still waits
    collisions = [0] * k
    done, t, finish = set(), 0, []
    while len(done) < k:
        ready = [s for s in range(k) if s not in done and wait[s] == 0]
        if len(ready) == 1:
            done.add(ready[0])
            finish.append(t + 1)
        elif len(ready) > 1:                  # a collision: everyone in it backs off
            for s in ready:
                collisions[s] += 1
                wait[s] = rng.randrange(2 ** min(collisions[s], cap)) + 1
        for s in range(k):
            if s not in done and wait[s] > 0:
                wait[s] -= 1
        t += 1
    return t, sum(finish) / k


if __name__ == "__main__":
    rng = random.Random(802)
    print(" k  slots to finish  mean delay of a frame (slots)")
    for k in (2, 4, 8, 16, 32):
        runs = [run(k, rng) for _ in range(2000)]
        total = sum(r[0] for r in runs) / len(runs)
        delay = sum(r[1] for r in runs) / len(runs)
        print(f"{k:2} {total:16.1f} {delay:14.1f}")
