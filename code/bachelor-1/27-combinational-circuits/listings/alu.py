"""alu.py: a 4-bit arithmetic and logic unit: two bits of operation code choose AND, OR,
addition or subtraction; four flags describe the result."""

from adders import full_adder
from circuit import Circuit, bits

OPS = {"AND": (0, 0), "OR": (0, 1), "ADD": (1, 0), "SUB": (1, 1)}  # (op1, op0)


def mux(c, s, x0, x1):
    """x1 if s else x0."""
    return c.gate("OR", c.gate("AND", c.gate("NOT", s), x0), c.gate("AND", s, x1))


def alu():
    c = Circuit(*[f"a{i}" for i in range(4)], *[f"b{i}" for i in range(4)],
                "op1", "op0")
    sub = c.gate("AND", "op1", "op0")
    carry, result = sub, []  # a - b = a + (not b) + 1
    for i in range(4):
        b = c.gate("XOR", f"b{i}", sub)
        s, carry = full_adder(c, f"a{i}", b, carry)
        both, either = c.gate("AND", f"a{i}", f"b{i}"), c.gate("OR", f"a{i}", f"b{i}")
        logic = mux(c, "op0", both, either)
        result.append(mux(c, "op1", logic, s))
        if i == 3:
            same_signs = c.gate("NOT", c.gate("XOR", "a3", b))
            overflow = c.gate("AND", "op1", same_signs, c.gate("XOR", s, "a3"))
    for i, r in enumerate(result):
        c.outputs[f"r{i}"] = r
    c.outputs |= {"Z": c.gate("NOR", *result), "N": result[3],
                  "C": c.gate("AND", "op1", carry), "V": overflow}
    return c


def run(c, op, x, y):
    values = {f"a{i}": v for i, v in enumerate(bits(x, 4))}
    values |= {f"b{i}": v for i, v in enumerate(bits(y, 4))}
    values |= dict(zip(("op1", "op0"), OPS[op]))
    out = c.evaluate(values)
    return sum(out[f"r{i}"] << i for i in range(4)), {f: out[f] for f in "ZNCV"}


def signed(v):
    return v - 16 if v >= 8 else v


def expected(op, x, y):
    r = {"AND": x & y, "OR": x | y, "ADD": x + y, "SUB": x - y}[op]
    exact = {"ADD": signed(x) + signed(y), "SUB": signed(x) - signed(y)}.get(op)
    flags = {"Z": int(r % 16 == 0), "N": (r % 16) >> 3,
             "C": int(op == "ADD" and r > 15 or op == "SUB" and x >= y),
             "V": int(exact is not None and not -8 <= exact <= 7)}
    return r % 16, flags


if __name__ == "__main__":
    c = alu()
    ok = all(run(c, op, x, y) == expected(op, x, y)
             for op in OPS for x in range(16) for y in range(16))
    print(f"{c.size()} gates, delay {c.delay()}; all 1024 cases correct: {ok}")
    for op, x, y in (("ADD", 2, 3), ("ADD", 7, 1), ("ADD", 9, 9), ("SUB", 5, 7),
                     ("SUB", 6, 6),
                     ("AND", 12, 10), ("OR", 12, 10)):
        r, flags = run(c, op, x, y)
        print(f"{op:3} {x:2} {y:2} -> {r:2} = {r:04b}  "
              + " ".join(f"{f}={v}" for f, v in flags.items()))
