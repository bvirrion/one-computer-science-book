"""Exercise: a vending machine. An item costs 3; each clock cycle the input is a coin
of 1 or 2, or none (c1 c0 = 01, 10, 00). Mealy machine: the state is the credit
(0, 1 or 2, in A B); the outputs are 'give the item' (v) and 'give back 1' (r)."""

import sys
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
from seq import minimal_sop, sop_gates, sop_text, sop_value  # noqa: E402


def machine(credit, coin):
    """The state diagram, as a function: (next credit, v, r)."""
    total = credit + coin
    return (0, 1, total - 3) if total >= 3 else (total, 0, 0)


def equations():
    rows = {}  # (A, B, c1, c0) as a number -> (A+, B+, v, r)
    for credit, coin in product(range(3), range(3)):
        nxt, v, r = machine(credit, coin)
        rows[credit * 4 + coin] = (nxt >> 1, nxt & 1, v, r)
    unused = [m for m in range(16) if m not in rows]  # credit 3 or coin code 11
    return [minimal_sop([m for m, out in rows.items() if out[i]], unused, 4)
            for i in range(4)]


def simulate(eqs, coins):
    q, out = (0, 0), []
    for coin in coins:
        x = (*q, coin >> 1, coin & 1)
        out.append((sop_value(eqs[2], x), sop_value(eqs[3], x)))
        q = (sop_value(eqs[0], x), sop_value(eqs[1], x))
    return out


def check(longest=8):
    eqs = equations()
    for k in range(longest + 1):
        for coins in product(range(3), repeat=k):
            credit, want = 0, []
            for coin in coins:
                credit, v, r = machine(credit, coin)
                want.append((v, r))
            if simulate(eqs, coins) != want:
                return False
    return True


if __name__ == "__main__":
    for name, e in zip(("A+", "B+", "v", "r"), equations()):
        print(f"{name:2} = {sop_text(e, ['A', 'B', 'c1', 'c0'])}")
    print("gates:", sop_gates(equations()),
          "| circuit = machine on all sequences of up to 8 coins:", check())
