"""ex12_sort.py -- insertion sort of four 4-bit values a0..a3, unrolled into
compare-and-swap steps, verified by bit-blasting the program itself: each variable is
a word of gates, and an if merges its two branches bit by bit with a multiplexer, so
the formula grows with the program instead of doubling at each if as wp does.
Verified: the result is sorted, every output is one of the inputs b0..b3 and every
input is one of the outputs."""

import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
sys.path.insert(
    0, str(Path(__file__).resolve().parents[2] / "18-hard-problems" / "listings")
)
from bitblast import Blaster  # noqa: E402
from cdcl import CDCL  # noqa: E402
from whilelang import parse  # noqa: E402


def program():
    lines = []
    for i in range(1, 4):  # insert a[i] into the sorted a[0..i-1]
        for j in range(i, 0, -1):
            lines += [
                f"if a{j - 1} > a{j}:",
                f"    t = a{j - 1}",
                f"    a{j - 1} = a{j}",
                f"    a{j} = t",
            ]
    return "\n".join(lines)


class Symbolic(Blaster):
    """Words of variables are looked up in an environment that execution updates."""

    def __init__(self):
        super().__init__()
        self.env = {}

    def word(self, e):
        if isinstance(e, ast.Name) and e.id in self.env:
            return self.env[e.id]
        return super().word(e)

    def mux(self, c, x, y):  # c ? x : y, bit by bit
        return [self.OR(self.AND(c, a), self.AND(-c, b)) for a, b in zip(x, y)]

    def execute(self, statements):
        for s in statements:
            if isinstance(s, ast.Assign):
                self.env[s.targets[0].id] = self.word(s.value)
            elif isinstance(s, ast.If):
                c, before = self.bit(s.test), dict(self.env)
                self.execute(s.body)
                after_yes, self.env = self.env, dict(before)
                self.execute(s.orelse)
                for x in set(after_yes) | set(self.env):
                    yes = after_yes.get(x, before.get(x))
                    no = self.env.get(x, before.get(x))
                    if yes is not None and no is not None and yes != no:
                        self.env[x] = self.mux(c, yes, no)


def one_of(x, ys):
    return "(" + " or ".join(f"{x} == {y}" for y in ys) + ")"


A, B = [f"a{k}" for k in range(4)], [f"b{k}" for k in range(4)]
POST = " and ".join(
    ["a0 <= a1", "a1 <= a2", "a2 <= a3"]
    + [one_of(a, B) for a in A]
    + [one_of(b, A) for b in B]
)


def verify(source=None):
    s = Symbolic()
    for k in range(4):
        s.env[f"a{k}"] = s.word(ast.Name(id=f"b{k}"))
    pre = s.bit(
        ast.parse(" and ".join(f"b{k} < 16" for k in range(4)), mode="eval").body
    )
    s.execute(parse(source or program()))
    post = s.bit(ast.parse(POST, mode="eval").body)
    s.clauses += [[pre], [-post]]  # a counterexample satisfies pre and not post
    model, _ = CDCL(s.clauses, s.n).solve()
    size = (s.n, len(s.clauses))
    if model is None:
        return True, None, size
    return (
        False,
        {
            x: sum(model[abs(v)] << i for i, v in enumerate(bits))
            for x, bits in sorted(s.words.items())
        },
        size,
    )


if __name__ == "__main__":
    print(verify())
    print(verify(program().replace("a2 > a3", "a2 < a3")))
