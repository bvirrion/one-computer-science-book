"""multitape.py -- palindromes on two tapes: copy the word to tape 2, rewind tape 1,
then read tape 1 forwards and tape 2 backwards. Steps against the one-tape machine."""
from machines import PALINDROME
from tm import BLANK as B
from tm import run


def run2(delta, word, start="q0", max_steps=100_000):
    """A two-tape machine: (state, (s1, s2)) -> (state, (w1, w2), (m1, m2))."""
    tapes, heads, state, steps = [dict(enumerate(word)), {}], [0, 0], start, 0
    while steps < max_steps:
        seen = tuple(t.get(h, B) for t, h in zip(tapes, heads))
        if (state, seen) not in delta:
            return state, steps
        state, written, moves = delta[(state, seen)]
        for t, h, w in zip(tapes, heads, written):
            t[h] = w
        heads = [h + {"L": -1, "R": 1, "S": 0}[m] for h, m in zip(heads, moves)]
        steps += 1
    return None, steps


PAL2 = {}
for x in "ab":
    PAL2[("copy", (x, B))] = ("copy", (x, x), ("R", "R"))  # copy, both move right
    PAL2[("rewind", (x, B))] = ("rewind", (x, B), ("L", "S"))  # tape 1 back to start
    for y in "ab":
        PAL2[("rewind", (x, y))] = ("rewind", (x, y), ("L", "S"))
        PAL2[("compare", (x, y))] = ("compare", (x, y), ("R", "L")) if x == y \
            else ("reject", (x, y), ("S", "S"))
PAL2[("copy", (B, B))] = ("rewind", (B, B), ("L", "L"))
for y in "ab" + B:
    PAL2[("rewind", (B, y))] = ("compare", (B, y), ("R", "S"))
PAL2[("compare", (B, B))] = ("accept", (B, B), ("S", "S"))

if __name__ == "__main__":
    print(" n   one tape   two tapes")
    for n in (2, 4, 8, 16, 32, 64, 128):
        w = ("ab" * n)[: n // 2]
        w += w[::-1]
        one = run(PALINDROME, w, max_steps=10**6)
        two = run2(PAL2, w, start="copy")
        assert one[1] == two[0] == "accept"
        print(f"{n:>3}   {one[3]:>8}   {two[1]:>9}")
