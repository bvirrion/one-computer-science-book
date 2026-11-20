"""nand_only.py: NOT, AND, OR and XOR built from NAND gates alone, checked on every
input."""

from itertools import product

from circuit import Circuit


def nand_not(c, x):
    return c.gate("NAND", x, x)


def nand_and(c, x, y):
    return nand_not(c, c.gate("NAND", x, y))


def nand_or(c, x, y):
    return c.gate("NAND", nand_not(c, x), nand_not(c, y))  # De Morgan


def nand_xor(c, x, y):
    n = c.gate("NAND", x, y)
    return c.gate("NAND", c.gate("NAND", x, n), c.gate("NAND", y, n))


if __name__ == "__main__":
    for name, build, spec in (("NOT", nand_not, lambda x, y: 1 - x),
                              ("AND", nand_and, lambda x, y: x & y),
                              ("OR", nand_or, lambda x, y: x | y),
                              ("XOR", nand_xor, lambda x, y: x ^ y)):
        c = Circuit("x", "y")
        c.outputs["out"] = build(c, "x") if name == "NOT" else build(c, "x", "y")
        ok = all(c.evaluate({"x": x, "y": y})["out"] == spec(x, y)
                 for x, y in product((0, 1), repeat=2))
        print(f"{name:3}: NAND gates {c.size()}, delay {c.delay()}, correct: {ok}")
