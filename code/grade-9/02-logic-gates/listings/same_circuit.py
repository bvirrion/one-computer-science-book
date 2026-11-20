from gates import AND, NOT, OR


def first(a, b):
    return NOT(AND(a, b))


def second(a, b):
    return OR(NOT(a), NOT(b))


agree = True
for a in [0, 1]:
    for b in [0, 1]:
        print(a, b, first(a, b), second(a, b))
        if first(a, b) != second(a, b):
            agree = False
print("the same on every input:", agree)
