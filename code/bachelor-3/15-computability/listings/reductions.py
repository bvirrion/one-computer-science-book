"""reductions.py -- from (M, w) build a machine M_w that erases its input, writes w and
runs M, accepting when M halts. M_w accepts the empty word exactly when M halts on w,
so a decider for "accepts the empty word" would decide the halting problem."""
from machines import INCREMENT
from tm import BLANK as B
from tm import accepts

RUN_RIGHT = {("q0", s): ("q0", s, "R") for s in "01" + B}  # never halts


def reduce(delta, w, alphabet="01"):
    tape = alphabet + B
    m = {("erase", s): ("erase", B, "R") for s in alphabet}  # wipe any input
    m[("erase", B)] = ("w0", B, "S")
    for i, c in enumerate(w):  # write w, one state per letter
        m[(f"w{i}", B)] = (f"w{i + 1}", c, "R")
    m[(f"w{len(w)}", B)] = ("b0", B, "L")
    for j in range(len(w)):  # walk back to the first letter of w
        for s in tape:
            m[(f"b{j}", s)] = (f"b{j + 1}", s, "L" if j + 1 < len(w) else "S")
    for s in tape:
        m[(f"b{len(w)}", s)] = (("M", "q0"), s, "S")
    states = {q for q, _ in delta} | {r for r, _, _ in delta.values()}
    for q in states:  # M's transitions, and "accept" wherever M halts
        for s in tape:
            r = delta.get((q, s))
            m[(("M", q), s)] = (("M", r[0]), r[1], r[2]) if r else ("accept", s, "S")
    return m


if __name__ == "__main__":
    print("M_w accepts the empty word / the word 0110, within 10,000 steps:")
    for name, delta, w in (("INCREMENT", INCREMENT, "1011"),
                           ("RUN_RIGHT", RUN_RIGHT, "1")):
        m = reduce(delta, w)
        answers = [accepts(m, x, start="erase", max_steps=10_000) for x in ("", "0110")]
        print(f"  M = {name}, w = {w}: {len(m)} transitions, {answers}")
