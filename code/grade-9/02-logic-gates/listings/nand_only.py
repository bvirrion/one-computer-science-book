def NAND(a, b):
    return 1 - a * b


def NOT(a):
    return NAND(a, a)


def AND(a, b):
    return NOT(NAND(a, b))


def OR(a, b):
    return NAND(NOT(a), NOT(b))


for a in [0, 1]:
    for b in [0, 1]:
        print(a, b, "| NAND", NAND(a, b), " AND", AND(a, b), " OR", OR(a, b),
              " NOT a", NOT(a))
