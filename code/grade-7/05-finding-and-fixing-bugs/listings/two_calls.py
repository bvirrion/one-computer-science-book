def average(values):
    total = 0
    for value in values:
        total = total + value
    return total / len(values)


def report(name, values):
    print(name, "average:", average(values))


report("Leo", [12, 10, 11, 9, 11])
report("Mia", [])
