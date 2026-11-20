def NOT(a):
    return 1 - a


def AND(a, b):
    return a * b


def OR(a, b):
    return a + b - a * b


def XOR(a, b):
    return (a + b) % 2


if __name__ == "__main__":
    print("a b | AND OR XOR")
    for a in [0, 1]:
        for b in [0, 1]:
            print(f"{a} {b} |  {AND(a, b)}   {OR(a, b)}   {XOR(a, b)}")
    print("NOT 0 =", NOT(0), " NOT 1 =", NOT(1))
