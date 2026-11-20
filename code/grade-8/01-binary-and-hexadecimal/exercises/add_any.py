def add_binary(a, b):
    """Add two strings of bits of any lengths."""
    while len(a) < len(b):
        a = "0" + a
    while len(b) < len(a):
        b = "0" + b
    result = ""
    carry = 0
    for i in range(len(a) - 1, -1, -1):
        total = int(a[i]) + int(b[i]) + carry
        result = str(total % 2) + result
        carry = total // 2
    if carry == 1:
        result = "1" + result
    return result


print(add_binary("1011", "110"), add_binary("1", "1111"))
