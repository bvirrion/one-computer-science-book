"""bitblast.py -- formulas over 8-bit unsigned variables turned into CNF, one Boolean
variable per bit and gate (Tseitin's encoding). A formula is valid when its negation
is unsatisfiable; a satisfying assignment of the negation is a counterexample."""

import ast
import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[2] / "18-hard-problems" / "listings")
)
from cdcl import CDCL  # noqa: E402

from whilelang import BITS  # noqa: E402


class Blaster:
    def __init__(self):
        self.clauses, self.n, self.words = [], 1, {}
        self.clauses.append([1])  # variable 1 is the constant true

    def fresh(self):
        self.n += 1
        return self.n

    def AND(self, a, b):
        g = self.fresh()  # g <-> a and b
        self.clauses += [[-g, a], [-g, b], [g, -a, -b]]
        return g

    def OR(self, a, b):
        return -self.AND(-a, -b)

    def XOR(self, a, b):
        g = self.fresh()
        self.clauses += [[-g, a, b], [-g, -a, -b], [g, -a, b], [g, a, -b]]
        return g

    def add(self, x, y, carry=-1):  # carry -1 is the constant false
        out = []
        for a, b in zip(x, y):  # ripple-carry, least significant bit first
            t = self.XOR(a, b)
            out.append(self.XOR(t, carry))
            carry = self.OR(self.AND(a, b), self.AND(t, carry))
        return out, carry

    def word(self, e):
        match e:
            case ast.Constant(value=c):
                return [1 if c >> i & 1 else -1 for i in range(BITS)]
            case ast.Name(id=x):
                if x not in self.words:
                    self.words[x] = [self.fresh() for _ in range(BITS)]
                return self.words[x]
            case ast.BinOp(left=a, op=ast.Add(), right=b):
                return self.add(self.word(a), self.word(b))[0]
            case ast.BinOp(left=a, op=ast.Sub(), right=b):  # a + not b + 1
                return self.add(self.word(a), [-v for v in self.word(b)], 1)[0]
            case ast.BinOp(left=a, op=ast.FloorDiv()):  # // 2: shift right
                return self.word(a)[1:] + [-1]
        raise ValueError(ast.unparse(e))

    def less(self, a, b):
        """a < b (unsigned) exactly when a - b borrows: a + not b + 1 has no carry."""
        return -self.add(self.word(a), [-v for v in self.word(b)], 1)[1]

    def equal(self, a, b):
        bit = 1
        for x, y in zip(self.word(a), self.word(b)):
            bit = self.AND(bit, -self.XOR(x, y))
        return bit

    def bit(self, e):
        match e:
            case ast.Constant(value=bool(c)):
                return 1 if c else -1
            case ast.UnaryOp(op=ast.Not(), operand=a):
                return -self.bit(a)
            case ast.BoolOp(op=op, values=[first, *rest]):
                out = self.bit(first)
                for v in rest:
                    out = (self.AND if isinstance(op, ast.And) else self.OR)(
                        out, self.bit(v)
                    )
                return out
            case ast.Call(func=ast.Name(id="implies"), args=[a, b]):
                return self.OR(-self.bit(a), self.bit(b))
            case ast.Compare(left=a, ops=[op], comparators=[b]):
                return {
                    ast.Lt: lambda: self.less(a, b),
                    ast.Gt: lambda: self.less(b, a),
                    ast.LtE: lambda: -self.less(b, a),
                    ast.GtE: lambda: -self.less(a, b),
                    ast.Eq: lambda: self.equal(a, b),
                    ast.NotEq: lambda: -self.equal(a, b),
                }[type(op)]()
        raise ValueError(ast.unparse(e))


def check(formula):
    """(True, size) if valid; else (False, counterexample values, size)."""
    b = Blaster()
    b.clauses.append([-b.bit(formula)])  # look for an assignment making it false
    model, _ = CDCL(b.clauses, b.n).solve()
    size = (b.n, len(b.clauses))
    if model is None:
        return True, None, size
    values = {
        x: sum(model[abs(v)] << i for i, v in enumerate(bits))
        for x, bits in sorted(b.words.items())
    }
    return False, values, size
