"""self_reduce.py -- finding a satisfying assignment with only a yes/no oracle for SAT.
A formula is a list of clauses; a clause is a list of literals, +i for x_i, -i for
not x_i. Fixing x_i to a value simplifies the formula; one oracle call per variable."""
import itertools
import random

calls = 0


def satisfiable(clauses, n):
    """The oracle: an exhaustive decision procedure. Only its answer is used."""
    global calls
    calls += 1
    return any(all(any((lit > 0) == bits[abs(lit) - 1] for lit in c) for c in clauses)
               for bits in itertools.product((False, True), repeat=n))


def fix(clauses, i, value):
    """Set x_i: drop the satisfied clauses, remove the literal from the others. An
    emptied clause stays, as an empty clause, which no assignment satisfies."""
    lit = i if value else -i
    return [[x for x in c if x != -lit] for c in clauses if lit not in c]


def find_assignment(clauses, n):
    if not satisfiable(clauses, n):
        return None
    values = []
    for i in range(1, n + 1):
        trial = fix(clauses, i, True)
        if satisfiable(trial, n):  # keep x_i = True if the rest can still be satisfied
            clauses, value = trial, True
        else:  # otherwise x_i = False must work, since the formula was satisfiable
            clauses, value = fix(clauses, i, False), False
        values.append(value)
    return values


if __name__ == "__main__":
    rng = random.Random(16)
    for n in (6, 8, 10, 12):
        clauses = [[rng.choice((1, -1)) * v for v in rng.sample(range(1, n + 1), 3)]
                   for _ in range(4 * n)]
        calls = 0
        a = find_assignment(clauses, n)
        ok = a is not None and all(any((x > 0) == a[abs(x) - 1] for x in c)
                                   for c in clauses)
        print(f"n = {n:>2}, {4 * n} clauses: "
              f"{'satisfiable' if a else 'unsatisfiable'}, {calls} oracle calls"
              + (f", assignment checked: {ok}" if a else ""))
    calls = 0
    every_sign = [[sx * 1, sy * 2, sz * 3] for sx in (1, -1) for sy in (1, -1)
                  for sz in (1, -1)]  # each clause forbids one of the 8 assignments
    print(f"n =  3, 8 clauses: {find_assignment(every_sign, 3)}, {calls} oracle call")
