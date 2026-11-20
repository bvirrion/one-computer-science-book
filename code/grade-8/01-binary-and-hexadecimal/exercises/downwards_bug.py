n = 6
bits = ""
while n > 0:
    bits = bits + str(n % 2)
    n = n // 2
print(bits)
