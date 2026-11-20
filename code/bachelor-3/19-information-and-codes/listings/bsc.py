"""bsc.py -- a binary symmetric channel, simulated with a seeded generator: each bit is
flipped with probability p. Repetition codes send each bit n times and decode by
majority; the bit error rate is measured and compared with the exact value."""
import random
from math import comb


def channel(bits, p, rng):
    return [b ^ (rng.random() < p) for b in bits]


def repetition_error(n, p):
    """A majority of n copies is wrong when more than n/2 of them are flipped."""
    return sum(comb(n, k) * p ** k * (1 - p) ** (n - k)
               for k in range(n // 2 + 1, n + 1))


if __name__ == "__main__":
    rng, trials = random.Random(19), 100_000
    print("   p   n  rate   measured   exact")
    for p in (0.01, 0.05, 0.1, 0.2):
        for n in (1, 3, 5):
            message = [rng.randrange(2) for _ in range(trials)]
            sent = [b for b in message for _ in range(n)]
            received = channel(sent, p, rng)
            decoded = [int(2 * sum(received[i:i + n]) > n)
                       for i in range(0, len(sent), n)]
            measured = sum(a != b for a, b in zip(message, decoded)) / trials
            exact = repetition_error(n, p)
            print(f"{p:>4}  {n:>2}  1/{n}  {measured:>9.5f}  {exact:.5f}")
