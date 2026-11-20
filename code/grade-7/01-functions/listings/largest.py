def largest2(a, b):
    if a > b:
        return a
    return b


def largest3(a, b, c):
    return largest2(largest2(a, b), c)


print(largest2(4, 9))
print(largest3(4, 9, 2))
print(largest3(7, 3, 5))
