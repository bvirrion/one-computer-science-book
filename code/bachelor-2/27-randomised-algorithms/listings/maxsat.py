"""maxsat.py: a uniformly random assignment against clauses of one, two and three
literals; the expected number satisfied is the sum of 1 - 2^-(length)."""
import random

rng = random.Random(4)
N = 30  # variables 1..30; the literal -v is "not v"


def clause(length):
    variables = rng.sample(range(1, N + 1), length)
    return [v if rng.random() < 0.5 else -v for v in variables]


def satisfied(clauses, x):
    return sum(any(x[abs(lit)] == (lit > 0) for lit in c) for c in clauses)


for lengths in [[2] * 200, [1] * 40 + [2] * 60 + [3] * 100]:
    clauses = [clause(k) for k in lengths]
    expected = sum(1 - 2 ** -len(c) for c in clauses)
    runs = [satisfied(clauses, [None] + [rng.random() < 0.5 for _ in range(N)])
            for _ in range(1000)]
    print(f"{len(clauses)} clauses: mean satisfied {sum(runs) / 1000:6.1f},"
          f" expected {expected:6.1f}, best of 1,000 runs {max(runs)}")
