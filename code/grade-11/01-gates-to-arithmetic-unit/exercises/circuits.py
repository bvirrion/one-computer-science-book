"""Exercises 5, 6, 7, 10, 11 and 14."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "listings"))
from full_adder import half_adder  # noqa: E402
from gates import AND, NOT, OR  # noqa: E402
from mux import mux2  # noqa: E402
from ripple import add_bits, from_bits, to_bits  # noqa: E402
from subtract import sub_bits  # noqa: E402


def half_adder_no_xor(a, b):  # exercise 5: XOR = (a OR b) AND NOT (a AND b)
    carry = AND(a, b)
    return AND(OR(a, b), NOT(carry)), carry


def full_adder_buggy(a, b, c):  # exercise 6: AND where XOR was meant
    s1, c1 = AND(a, b), AND(a, b)
    s, c2 = half_adder(s1, c)
    return s, OR(c1, c2)


def mux4(sel, inputs):  # exercise 7: sel is 0..3
    s1, s0 = (sel >> 1) & 1, sel & 1
    return mux2(s1, mux2(s0, inputs[0], inputs[1]), mux2(s0, inputs[2], inputs[3]))


def sub_bits_buggy(a, b):  # exercise 10: flips b but forgets the + 1
    return add_bits(a, [NOT(bit) for bit in b], carry=0)


def alu_reference(op, x, y):  # exercise 11: the same ALU with Python's integers
    if op == "AND":
        r, c = x & y, 0
    elif op == "OR":
        r, c = x | y, 0
    elif op == "ADD":
        r, c = (x + y) % 256, int(x + y > 255)
    else:
        r, c = (x - y) % 256, int(x < y)
    return r, {"Z": int(r == 0), "N": r >> 7, "C": c}


def comparator(x, y, n=8):  # exercise 14: from the flags of x - y
    bits, carries = sub_bits(to_bits(x, n), to_bits(y, n))
    if from_bits(bits) == 0:
        return "="
    return "<" if carries[n] == 0 else ">"  # no carry out: a borrow, so x < y
