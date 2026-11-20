def add_binary(a, b):
    """Add two strings of bits of the same length, column by column from the right."""
    result = ""
    carry = 0
    for i in range(len(a) - 1, -1, -1):
        total = int(a[i]) + int(b[i]) + carry
        result = str(total % 2) + result
        carry = total // 2
    if carry == 1:
        result = "1" + result
    return result


print(add_binary("01101101", "00111011"))
print(add_binary("11001000", "01110000"))
