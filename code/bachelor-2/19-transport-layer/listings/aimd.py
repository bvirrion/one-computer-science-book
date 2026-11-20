"""aimd.py: a congestion window per round trip; the throughput law checked."""
import math
import random


def rounds(n, p, periodic=True, seed=0, ssthresh=64.0):
    """Yield the window of each round trip: slow start, then +1, halved on a loss."""
    rng, w, sent, next_loss = random.Random(seed), 1.0, 0, 1 / p
    for _ in range(n):
        yield w
        k = int(w)
        if periodic:
            lost = sent + k >= next_loss         # the (1/p)-th packet is lost
            next_loss += (1 / p) if lost else 0
        else:
            lost = any(rng.random() < p for _ in range(k))
        sent += k
        if lost:
            w = ssthresh = max(w / 2, 1.0)       # multiplicative decrease
        elif w < ssthresh:
            w *= 2                               # slow start
        else:
            w += 1                               # additive increase


if __name__ == "__main__":
    print("     p   sqrt(3/2p)  periodic  error   random  error  (packets per RTT)")
    for p in (0.01, 0.003, 0.001, 0.0003):
        law = math.sqrt(3 / (2 * p))
        per = sum(int(w) for w in rounds(200_000, p)) / 200_000
        ran = sum(int(w) for w in rounds(200_000, p, periodic=False, seed=5)) / 200_000
        print(f"{p:6}  {law:10.2f}  {per:8.2f}  {per / law - 1:+5.1%}"
              f"  {ran:7.2f}  {ran / law - 1:+5.1%}")
