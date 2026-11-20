from gates import AND, NOT, OR


def circuit(a, b, c):
    """(a AND b) OR (NOT c)"""
    return OR(AND(a, b), NOT(c))


print("a b c | out")
for a in [0, 1]:
    for b in [0, 1]:
        for c in [0, 1]:
            print(a, b, c, "|", circuit(a, b, c))
