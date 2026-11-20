def largest(values):
    best = 0
    for i in range(1, len(values)):
        if values[i] > best:
            best = values[i]
    return best


print(largest([3, 9, 4]), largest([9, 3, 4]), largest([5]))
