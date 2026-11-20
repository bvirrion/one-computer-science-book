def average(values):
    if len(values) == 0:
        return 0
    total = 0
    for value in values:
        total = total + value
    return total / len(values)


print(average([12, 10, 11, 9, 11]), average([]))
