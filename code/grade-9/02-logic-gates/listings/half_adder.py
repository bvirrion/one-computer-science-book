from gates import AND, XOR


def half_adder(a, b):
    """Add two bits: the sum bit and the carry bit."""
    return XOR(a, b), AND(a, b)


print("a + b = carry sum")
for a in [0, 1]:
    for b in [0, 1]:
        total, carry = half_adder(a, b)
        print(a, "+", b, "=", carry, total)
