def average(marks):
    total = 0
    for mark in marks:
        total = total + mark
        print("  trace: mark", mark, "total", total)
    print("  trace: dividing", total, "by 4")
    return total / 4


print(average([12, 10, 11, 9, 11]))
