"""aloha_sim.py: slotted ALOHA, simulated; throughput against G e^-G."""
import math
import random


def throughput(G, stations=100, slots=20_000, rng=random):
    """Fraction of slots that carry exactly one frame, G frames tried per slot."""
    p = G / stations
    good = 0
    for _ in range(slots):
        senders = sum(rng.random() < p for _ in range(stations))
        good += senders == 1
    return good / slots


if __name__ == "__main__":
    rng = random.Random(1971)
    print("   G  simulated  G e^-G")
    for k in range(1, 13):
        G = k / 4
        print(f"{G:4.2f}  {throughput(G, rng=rng):9.3f}  {G * math.exp(-G):6.3f}")
