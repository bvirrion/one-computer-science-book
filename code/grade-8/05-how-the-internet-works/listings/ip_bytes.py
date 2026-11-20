address = "192.168.1.20"
parts = address.split(".")
bits = ""
for part in parts:
    byte = int(part)
    print(part.rjust(3), "->", f"{byte:08b}")
    bits = bits + f"{byte:08b}"
print(len(parts), "bytes,", len(bits), "bits:", bits)
