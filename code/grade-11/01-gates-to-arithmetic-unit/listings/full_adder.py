from gates import AND, OR, XOR


def half_adder(a, b):
    """Two bits in; their sum bit and their carry out."""
    return XOR(a, b), AND(a, b)


def full_adder(a, b, c):
    """Three bits in (c is the carry from the column before); sum and carry out."""
    s1, c1 = half_adder(a, b)
    s, c2 = half_adder(s1, c)
    return s, OR(c1, c2)


if __name__ == "__main__":
    print("a b c | s carry | a+b+c")
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                s, carry = full_adder(a, b, c)
                assert 2 * carry + s == a + b + c   # checked on all 8 rows
                print(f"{a} {b} {c} | {s}   {carry}   |   {a + b + c}")
