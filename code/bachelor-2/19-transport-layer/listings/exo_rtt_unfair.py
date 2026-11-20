"""exo_rtt_unfair.py: flow 2's round trip is twice flow 1's (exercise 11)."""
from fairness import jain

w1, w2, capacity, sum1, sum2 = 10.0, 10.0, 60.0, 0.0, 0.0
for step in range(20_000):                       # one step = flow 1's round trip
    r1, r2 = w1, w2 / 2                          # rates: window per round trip
    if r1 + r2 > capacity:
        w1, w2 = w1 / 2, w2 / 2                  # a shared loss halves both
    else:
        w1 += 1                                  # flow 1: one more every round trip
        w2 += 1 if step % 2 else 0               # flow 2: one more every two steps
    if step >= 10_000:
        sum1, sum2 = sum1 + r1, sum2 + r2
s = sum1 / (sum1 + sum2)
print(f"shares of the link: flow 1 {s:.3f}, flow 2 {1 - s:.3f}")
print(f"fairness index: {jain([sum1, sum2]):.3f}")
