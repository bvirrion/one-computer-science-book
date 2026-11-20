"""moore_mealy.py: Mealy and Moore machines, the conversions between them, and a check
that a machine and its conversion give the same output on every input word."""

from seq import all_words


class Mealy:
    """delta[state, symbol] = (next state, output): the output is on the transition."""

    def __init__(self, start, delta):
        self.start, self.delta = start, delta

    def run(self, word):
        q, out = self.start, []
        for a in word:
            q, o = self.delta[q, a]
            out.append(o)
        return out


class Moore:
    """delta[state, symbol] = next state; out[state]: the output is the state's."""

    def __init__(self, start, delta, out):
        self.start, self.delta, self.out = start, delta, out

    def run(self, word):  # the outputs of the states entered, one per symbol
        q, out = self.start, []
        for a in word:
            q = self.delta[q, a]
            out.append(self.out[q])
        return out


def mealy_to_moore(m, alphabet):
    """A Moore state (q, o): in q, having just output o. Only the reachable ones."""
    first = (m.start, 0)
    states, todo, delta = {first}, [first], {}
    while todo:
        q, o = todo.pop()
        for a in alphabet:
            nxt = m.delta[q, a]
            delta[(q, o), a] = nxt
            if nxt not in states:
                states.add(nxt)
                todo.append(nxt)
    return Moore(first, delta, {s: s[1] for s in states})


def moore_to_mealy(m):
    """Output, on a transition, the output of the state it enters."""
    return Mealy(m.start, {(q, a): (r, m.out[r]) for (q, a), r in m.delta.items()})


def same_outputs(m1, m2, alphabet, longest):
    return all(m1.run(w) == m2.run(w) for w in all_words(alphabet, longest))


# Detect 101 in a stream of bits, overlaps allowed: output 1 at the last 1.
DETECT_101 = Mealy("-", {("-", 0): ("-", 0), ("-", 1): ("1", 0),
                         ("1", 0): ("10", 0), ("1", 1): ("1", 0),
                         ("10", 0): ("-", 0), ("10", 1): ("1", 1)})

if __name__ == "__main__":
    moore = mealy_to_moore(DETECT_101, (0, 1))
    for (q, o), a in sorted(moore.delta):
        r = moore.delta[(q, o), a]
        print(f"Moore ({q:>2}, {o}) --{a}--> ({r[0]:>2}, {r[1]})")
    print(f"Mealy states: {len({q for q, _ in DETECT_101.delta})}, "
          f"Moore states: {len(moore.out)}")
    back = moore_to_mealy(moore)
    print("Mealy and Moore agree on all 2047 words of length <= 10:",
          same_outputs(DETECT_101, moore, (0, 1), 10))
    print("and the Mealy machine made back from it:",
          same_outputs(DETECT_101, back, (0, 1), 10))
    print("on 0110101101:", DETECT_101.run([0, 1, 1, 0, 1, 0, 1, 1, 0, 1]))
