"""lock.py: a lock that opens on the key sequence 1 0 1 1, keys pressed one at a time.
Its Mealy and Moore machines; distinguishing words, which prove each one minimal; and
both machines as circuits, checked on every word of up to 12 keys."""

from collections import deque

from moore_mealy import Mealy, mealy_to_moore
from seq import all_words, minimal_sop, sop_gates, sop_text, sop_value

KEYS = (0, 1)


def detector(pattern):
    """Mealy machine: the state is the longest prefix of the pattern that ends the
    keys pressed so far; output 1 when the whole pattern has just been pressed."""
    prefixes = [tuple(pattern[:i]) for i in range(len(pattern))]
    delta = {}
    for p in prefixes:
        for a in KEYS:
            w = p + (a,)
            done = int(w == tuple(pattern))
            nxt = next(w[i:] for i in range(len(w) + 1) if w[i:] in prefixes)
            delta[p, a] = (nxt, done)
    return Mealy((), delta)


def outputs(m, state, word):
    """Outputs of machine m started in state; a Moore machine also shows its own."""
    if isinstance(m, Mealy):
        return Mealy(state, m.delta).run(word)
    out, q = [m.out[state]], state
    for a in word:
        q = m.delta[q, a]
        out.append(m.out[q])
    return out


def distinguishing(m, states):
    """For each pair of states, a shortest word on which their outputs differ."""
    found = {}
    for i, p in enumerate(states):
        for q in states[i + 1:]:
            words = deque([()])
            while words:
                w = words.popleft()
                if outputs(m, p, w) != outputs(m, q, w):
                    found[p, q] = w
                    break
                if len(w) < len(states):
                    words.extend(w + (a,) for a in KEYS)
    return found


def as_circuit(states, step, out_of, nbits, with_key_in_output):
    """Number the states in binary; simplify each next-state bit and the output."""
    code = {s: i for i, s in enumerate(states)}
    n_in = nbits + 1
    unused = [c * 2 + a for c in range(len(states), 2 ** nbits) for a in KEYS]
    eqs = []
    for bit in reversed(range(nbits)):
        ones = [code[s] * 2 + a for s in states for a in KEYS
                if code[step(s, a)] >> bit & 1]
        eqs.append(minimal_sop(ones, unused, n_in))
    if with_key_in_output:
        z = minimal_sop([code[s] * 2 + a for s in states for a in KEYS if out_of(s, a)],
                        unused, n_in)
    else:
        z = minimal_sop([code[s] for s in states if out_of(s, None)],
                        range(len(states), 2 ** nbits), nbits)
    return code, eqs, z


def circuit_run(eqs, z, nbits, with_key_in_output, word):
    q, out = (0,) * nbits, []
    for a in word:
        if with_key_in_output:
            out.append(sop_value(z, (*q, a)))
        q = tuple(sop_value(e, (*q, a)) for e in eqs)
        if not with_key_in_output:
            out.append(sop_value(z, q))
    return out


if __name__ == "__main__":
    mealy = detector([1, 0, 1, 1])
    moore = mealy_to_moore(mealy, KEYS)
    show = {(): "e", (1,): "1", (1, 0): "10", (1, 0, 1): "101"}
    moore_states = sorted(moore.out, key=lambda s: (s[1], len(s[0])))
    kinds = [("Mealy", mealy, sorted(show, key=len), 2, True,
              lambda s, a: mealy.delta[s, a][0], lambda s, a: mealy.delta[s, a][1]),
             ("Moore", moore, moore_states, 3, False,
              lambda s, a: moore.delta[s, a], lambda s, a: moore.out[s])]
    for kind, m, states, nbits, mealy_out, step, out_of in kinds:
        def name(s, kind=kind):
            return show[s] if kind == "Mealy" else f"{show[s[0]]}/{s[1]}"
        print(f"{kind}: {len(states)} states:", ", ".join(name(s) for s in states))
        pairs = distinguishing(m, states)
        shown = [f"{name(p)}~{name(q)} '{''.join(map(str, w))}'"
                 for (p, q), w in pairs.items()]
        print(f"  {len(pairs)} pairs of states, each with a word telling them apart:")
        for i in range(0, len(shown), 5):
            print("    " + ", ".join(shown[i:i + 5]))
        code, eqs, z = as_circuit(states, step, out_of, nbits, mealy_out)
        names = "ABx" if nbits == 2 else "ABCx"
        for i, e in enumerate(eqs):
            print(f"  {names[i]}+ = {sop_text(e, names)}")
        print(f"  z  = {sop_text(z, names if mealy_out else names[:-1])}")
        ok = all(circuit_run(eqs, z, nbits, mealy_out, w) == m.run(w)
                 for w in all_words(KEYS, 12))
        print(f"  flip-flops {nbits}, gates {sop_gates(eqs + [z])}; "
              f"circuit = machine on all words of up to 12 keys: {ok}")
