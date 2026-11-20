from full_adder import full_adder
from gates import AND, NOT, OR, XOR
from mux import mux4
from ripple import from_bits, to_bits

OPS = {"AND": (0, 0), "OR": (0, 1), "ADD": (1, 0), "SUB": (1, 1)}


def alu(op, a, b):
    """8-bit ALU: every column computes all four results, a multiplexer keeps one."""
    s1, s0 = OPS[op]
    carry = s0  # SUB adds 1 through the first carry
    out = []
    for x, y in zip(a, b):
        y2 = XOR(y, AND(s1, s0))  # flip b only for SUB
        s, carry = full_adder(x, y2, carry)
        out.append(mux4(s1, s0, [AND(x, y), OR(x, y), s, s]))
    zero = NOT(OR(OR(OR(out[0], out[1]), OR(out[2], out[3])),
                  OR(OR(out[4], out[5]), OR(out[6], out[7]))))
    c = AND(s1, XOR(carry, s0))  # ADD: the carry; SUB: no carry means a borrow
    return out, {"Z": zero, "N": out[7], "C": c}


if __name__ == "__main__":
    for op, x, y in [("AND", 12, 10), ("OR", 12, 10), ("ADD", 250, 10),
                     ("SUB", 5, 10), ("SUB", 10, 10)]:
        bits, flags = alu(op, to_bits(x, 8), to_bits(y, 8))
        print(f"{op:3} {x:3} {y:3} -> {from_bits(bits):3}  {flags}")
