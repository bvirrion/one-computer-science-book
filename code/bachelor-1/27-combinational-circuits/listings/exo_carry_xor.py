"""exo_carry_xor.py: exercise 6, a full adder whose carry is assembled differently."""

from itertools import product

from circuit import Circuit

c = Circuit("a", "b", "cin")
c.outputs["s"] = c.gate("XOR", c.gate("XOR", "a", "b"), "cin")
c.outputs["cout"] = c.gate("XOR", c.gate("AND", "a", "b"),
                           c.gate("AND", "cin", c.gate("OR", "a", "b")))

if __name__ == "__main__":
    for a, b, cin in product((0, 1), repeat=3):
        out = c.evaluate({"a": a, "b": b, "cin": cin})
        if out["s"] + 2 * out["cout"] != a + b + cin:
            print(f"wrong on a={a} b={b} cin={cin}: carry {out['cout']}")
