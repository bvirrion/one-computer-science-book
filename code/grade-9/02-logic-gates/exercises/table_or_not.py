from gates import AND, NOT, OR

for a in [0, 1]:
    for b in [0, 1]:
        for c in [0, 1]:
            print(a, b, c, "|", AND(OR(a, b), NOT(c)))
