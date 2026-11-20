"""tm.py -- a Turing machine simulator. A machine is a dict mapping (state, symbol) to
(new state, symbol written, move), the move being "L", "R" or "S" (stay). The blank is
"_". With no transition for the current pair, the machine halts; it accepts if it halts
in the state "accept"."""
BLANK = "_"


def config(tape, head, state):
    """The configuration u q v: the tape left of the head, the state, the rest."""
    lo, hi = min([*tape, head]), max([*tape, head])
    left = "".join(tape.get(i, BLANK) for i in range(lo, head))
    right = "".join(tape.get(i, BLANK) for i in range(head, hi + 1))
    return f"{left}[{state}]{right}"


def run(delta, word, start="q0", max_steps=10_000, trace=None):
    """Run on `word`; returns (halted, state, tape contents, steps)."""
    tape = {i: c for i, c in enumerate(word)}
    head, state, steps = 0, start, 0
    while (state, tape.get(head, BLANK)) in delta:
        if steps == max_steps:
            return False, state, contents(tape), steps
        if trace is not None:
            trace(config(tape, head, state))
        state, tape[head], move = delta[(state, tape.get(head, BLANK))]
        head += {"L": -1, "R": 1, "S": 0}[move]
        steps += 1
    if trace is not None:
        trace(config(tape, head, state))
    return True, state, contents(tape), steps


def contents(tape):
    """The tape between its first and last non-blank cells."""
    marked = [i for i, c in tape.items() if c != BLANK]
    if not marked:
        return ""
    return "".join(tape.get(i, BLANK) for i in range(min(marked), max(marked) + 1))


def accepts(delta, word, **kw):
    halted, state, _, _ = run(delta, word, **kw)
    return halted and state == "accept"
