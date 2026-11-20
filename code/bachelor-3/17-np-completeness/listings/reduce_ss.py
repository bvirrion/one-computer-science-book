"""reduce_ss.py -- 3-SAT to subset sum. Numbers are written in base 10 with one digit
per variable, then one per clause. Choosing y_i (x_i true) or z_i (x_i false) puts a 1
in digit i and in the digit of each clause the literal satisfies; two slack numbers per
clause can add up to 2 more. The target has 1 per variable and 3 per clause."""
import random

from cnf import brute_force, random_3cnf, subset_sums_to


def to_subset_sum(clauses, n):
    m = len(clauses)

    def number(var_digit, clause_digits):  # digits: variables first, then clauses
        digits = [0] * (n + m)
        if var_digit is not None:
            digits[var_digit] = 1
        for j in clause_digits:
            digits[n + j] += 1
        return int("".join(map(str, digits)))
    numbers = []
    for i in range(1, n + 1):
        numbers.append(number(i - 1, [j for j, c in enumerate(clauses) if i in c]))
        numbers.append(number(i - 1, [j for j, c in enumerate(clauses) if -i in c]))
    for j in range(m):
        numbers += [number(None, [j]), number(None, [j])]  # slack: at most 2 more
    target = int("1" * n + "3" * m)
    return numbers, target


if __name__ == "__main__":
    formula = [[1, -2, 3], [-1, 2, 3]]
    numbers, target = to_subset_sum(formula, 3)
    print("numbers:", numbers)
    print("target: ", target)
    rng, agree = random.Random(17), 0
    for _ in range(200):
        f = random_3cnf(4, rng.randrange(1, 7), rng)
        agree += (brute_force(f) is not None) == subset_sums_to(*to_subset_sum(f, 4))
    print(f"satisfiable = some subset reaches the target: {agree} of 200 "
          f"random formulas")
