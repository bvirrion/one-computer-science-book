"""stride.py -- fair share by lottery and by stride: three clients holding 100, 50 and
250 tickets. How far is each from its share of the quanta, after 10, 100 and 1,000 of
them?"""
import random

TICKETS = {"A": 100, "B": 50, "C": 250}
TOTAL = sum(TICKETS.values())
rng = random.Random(7)


def lottery():  # draw a ticket at random; its holder runs
    k = rng.randrange(TOTAL)
    for name, n in TICKETS.items():
        if k < n:
            return name
        k -= n


stride = {name: 10_000 // n for name, n in TICKETS.items()}  # big number / tickets
passes = dict(stride)


def stride_next():  # the least pass runs, and its pass advances by its stride
    name = min(passes, key=lambda c: (passes[c], c))
    passes[name] += stride[name]
    return name


counts = {"lottery": dict.fromkeys(TICKETS, 0), "stride": dict.fromkeys(TICKETS, 0)}
worst = {"lottery": 0.0, "stride": 0.0}
print(f"{'quanta':>6} {'ideal A B C':>20} {'lottery':>14} {'stride':>14}")
for q in range(1, 1001):
    counts["lottery"][lottery()] += 1
    counts["stride"][stride_next()] += 1
    for policy, c in counts.items():
        for name, n in TICKETS.items():
            worst[policy] = max(worst[policy], abs(c[name] - q * n / TOTAL))
    if q in (10, 100, 1000):
        ideal = " ".join(f"{q * n / TOTAL:g}" for n in TICKETS.values())
        cols = [" ".join(str(counts[p][name]) for name in TICKETS) for p in counts]
        print(f"{q:>6} {ideal:>20} {cols[0]:>14} {cols[1]:>14}")
print(f"largest error over the 1,000 quanta: lottery {worst['lottery']:.2f}, "
      f"stride {worst['stride']:.2f} quanta")
