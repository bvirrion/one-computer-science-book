"""detector.py: from a state diagram to a circuit. The Moore detector of 101 gets a
state encoding; its next-state and output functions are simplified as in chapter 27;
the circuit (two D flip-flops and gates) is checked against the machine."""

from moore_mealy import DETECT_101, mealy_to_moore
from seq import all_words, minimal_sop, sop_gates, sop_text, sop_value

MOORE = mealy_to_moore(DETECT_101, (0, 1))
CODE = {("-", 0): (0, 0), ("1", 0): (0, 1), ("10", 0): (1, 0), ("1", 1): (1, 1)}


def equations():
    """Next state bits A+, B+ as functions of (A, B, x); the output z of (A, B)."""
    ones = {0: [], 1: []}
    for (state, x), nxt in MOORE.delta.items():
        row = CODE[state][0] * 4 + CODE[state][1] * 2 + x
        for bit in (0, 1):
            if CODE[nxt][bit]:
                ones[bit].append(row)
    z = [CODE[s][0] * 2 + CODE[s][1] for s, o in MOORE.out.items() if o]
    return [minimal_sop(ones[0], [], 3), minimal_sop(ones[1], [], 3),
            minimal_sop(z, [], 2)]


def circuit_run(eqs, word):
    """Two D flip-flops (A, B), loaded at each clock edge; output z of the state."""
    d1, d0, z = eqs
    q, out = (0, 0), []
    for x in word:
        q = (sop_value(d1, (*q, x)), sop_value(d0, (*q, x)))
        out.append(sop_value(z, q))
    return out


if __name__ == "__main__":
    eqs = equations()
    for name, terms, names in zip(("A+", "B+", "z"), eqs, ("ABx", "ABx", "AB")):
        print(f"{name:2} = {sop_text(terms, names)}")
    print(f"gates: {sop_gates(eqs)}, flip-flops: 2")
    ok = all(circuit_run(eqs, w) == MOORE.run(w) for w in all_words((0, 1), 12))
    print("circuit = machine on all 8191 words of length <= 12:", ok)
