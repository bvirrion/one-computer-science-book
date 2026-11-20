grains = 1
total = 0
for square in range(1, 65):
    total = total + grains
    if square <= 8 or square == 64:
        print("square", square, ":", grains, "grains, total", total)
    grains = grains * 2

print("total:", total)
print("2 ** 64 - 1 =", 2 ** 64 - 1)
print("binary:", bin(total)[2:].count("1"), "ones,", len(bin(total)) - 2, "bits")
print("hexadecimal:", hex(total)[2:].upper())
