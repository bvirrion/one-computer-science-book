bits = "101100"
value = 0
for bit in bits:
    value = value * 2 + int(bit)     # shift one place left, then add the new bit
    print(bit, "->", value)
print(bits, "in binary is", value)
