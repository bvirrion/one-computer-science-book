# Two neighbouring digits a, b (weights 1 and 3) swapped to b, a.
caught = 0
for a in range(10):
    for b in range(10):
        if a != b:
            change = (b * 1 + a * 3) - (a * 1 + b * 3)
            if change % 10 != 0:
                caught = caught + 1
            else:
                print("missed:", a, b)
print(caught, "caught out of 90")
