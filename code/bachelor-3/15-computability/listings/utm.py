"""utm.py -- machines as strings, and one program that runs them all. A machine is
encoded over the alphabet {0, 1, #}: states and symbols are numbered, each number is
written in unary, and each transition is five numbers separated by 0s."""
from machines import INCREMENT
from tm import run

MOVES = "LRS"


def encode(delta, start="q0"):
    """The machine as a string <M>; the start state gets number 1."""
    named = {s for s, _ in delta} | {t for t, _, _ in delta.values()}
    states = [start] + sorted(named - {start})
    symbols = sorted({a for _, a in delta} | {b for _, b, _ in delta.values()})
    num = {**{s: i + 1 for i, s in enumerate(states)},
           **{("sym", a): i + 1 for i, a in enumerate(symbols)}}
    code = []
    for (q, a), (r, b, m) in sorted(delta.items()):
        fields = [num[q], num[("sym", a)], num[r], num[("sym", b)], MOVES.index(m) + 1]
        code.append("0".join("1" * f for f in fields))
    return "#".join(code), symbols


def universal(code, symbols, word):
    """Decode <M> and run it on word: one program for every machine."""
    delta = {}
    for t in code.split("#"):
        q, a, r, b, m = (len(f) for f in t.split("0"))
        delta[(q, symbols[a - 1])] = (r, symbols[b - 1], MOVES[m - 1])
    return run(delta, word, start=1)


if __name__ == "__main__":
    code, symbols = encode(INCREMENT)
    print(f"symbols {symbols} are 1, 2, 3; <INCREMENT> has {len(code)} characters")
    for t in code.split("#")[:2]:
        print(f"  {t:<20} = {[len(f) for f in t.split('0')]}")
    for w in ("1011", "111"):
        direct, via = run(INCREMENT, w)[2], universal(code, symbols, w)[2]
        print(f"on {w}: directly {direct}, through the universal program {via}")
