def average(marks):
    total = 0
    for mark in marks:
        total = total + mark
    return total / 4


print(average([12, 10, 11, 9, 11]))
