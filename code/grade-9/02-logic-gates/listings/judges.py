from gates import AND, OR


def spec(a, b, c):
    """The rule itself: at least two of the three judges press."""
    return int(a + b + c >= 2)


def pairs(a, b, c):
    """Any pair of judges pressing: (a AND b) OR (b AND c) OR (a AND c)."""
    return OR(OR(AND(a, b), AND(b, c)), AND(a, c))


def majority(a, b, c):
    """Another idea: a and b agree, or else c decides."""
    return OR(AND(a, b), AND(c, OR(a, b)))


print("a b c | spec pairs majority")
ok = True
for a in [0, 1]:
    for b in [0, 1]:
        for c in [0, 1]:
            row = [spec(a, b, c), pairs(a, b, c), majority(a, b, c)]
            print(a, b, c, "|", row[0], "   ", row[1], "    ", row[2])
            if row[0] != row[1] or row[0] != row[2]:
                ok = False
print("all three agree on the 8 inputs:", ok)
print("rows for five judges:", 2**5)
