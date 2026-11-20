def average(marks):
    total = 0
    for mark in marks:
        total = total + mark
    return total / len(marks)


print(average([12, 10, 11, 9, 11]))
