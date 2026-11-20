from gates import AND, NOT, OR


def mux2(s, x0, x1):
    """x0 if s is 0, x1 if s is 1."""
    return OR(AND(NOT(s), x0), AND(s, x1))


def mux4(s1, s0, x):
    """One of the four inputs x[0..3], chosen by the two bits s1 s0."""
    return mux2(s1, mux2(s0, x[0], x[1]), mux2(s0, x[2], x[3]))


def decoder2(s1, s0):
    """Four outputs; exactly the one numbered s1 s0 is 1."""
    n1, n0 = NOT(s1), NOT(s0)
    return [AND(n1, n0), AND(n1, s0), AND(s1, n0), AND(s1, s0)]


if __name__ == "__main__":
    x = [0, 1, 1, 0]
    print("inputs x0..x3 =", x)
    for s1 in (0, 1):
        for s0 in (0, 1):
            print(f"select {s1}{s0}: mux4 -> {mux4(s1, s0, x)}"
                  f"   decoder -> {decoder2(s1, s0)}")
