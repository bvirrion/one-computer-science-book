def area(width, length):
    return width * length


def largest2(a, b):
    if a > b:
        return a
    return b


# Each answer is worked out by hand first, then compared with the call.
print("expected 12, got", area(3, 4))
print("expected 0, got", area(0, 7))
print("expected 9, got", largest2(4, 9))
print("expected 9, got", largest2(9, 4))
print("expected 5, got", largest2(5, 5))
