for n in (1, 2, 255, 256, 1000, 65535, 65536):
    print(f"{n:6}  bit_length {n.bit_length():2}")

a = 2**20 - 1  # the largest number on 20 bits
b = 2**13 - 1  # the largest number on 13 bits
print("a + b needs", (a + b).bit_length(), "bits")
print("a * b needs", (a * b).bit_length(), "bits")
