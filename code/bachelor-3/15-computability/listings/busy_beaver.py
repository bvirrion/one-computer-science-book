"""busy_beaver.py -- every n-state, 2-symbol machine, run from the blank tape with a
step cap. Each of the 2n transitions writes 0 or 1, moves L or R, and goes to one of
the n states or to the halting state H. S(n): most steps before halting; Sigma(n): most
1s left on the tape."""
from itertools import product

CAP = 100


def run(machine, cap=CAP):
    """Steps and number of 1s if the machine halts within cap steps, else None."""
    tape, head, state = {}, 0, 0
    for step in range(1, cap + 1):
        write, move, state = machine[2 * state + tape.get(head, 0)]
        tape[head] = write
        head += move
        if state == "H":
            return step, sum(tape.values())
    return None


def busy_beaver(n):
    actions = list(product((0, 1), (-1, 1), [*range(n), "H"]))
    halting, best_s, best_sigma, champion = 0, 0, 0, None
    for machine in product(actions, repeat=2 * n):
        result = run(machine)
        if result is None:
            continue
        halting += 1
        best_s = max(best_s, result[0])
        if result[1] > best_sigma:
            best_sigma, champion = result[1], machine
    return len(actions) ** (2 * n), halting, best_s, best_sigma, champion


def name(machine):
    """1RB = write 1, move right, go to B; transitions for A0 A1 B0 B1 ..."""
    return " ".join(f"{w}{'LR'[m > 0]}{'ABCDEFGH'[q] if q != 'H' else 'H'}"
                    for w, m, q in machine)


if __name__ == "__main__":
    for n in (1, 2):
        total, halting, s, sigma, champion = busy_beaver(n)
        print(f"n = {n}: {total:,} machines, {halting:,} halt within {CAP} steps; "
              f"S({n}) = {s}, Sigma({n}) = {sigma}")
    print("a Sigma(2) champion:", name(champion))
