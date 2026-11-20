print("     " + " ".join(f"{c:X}" for c in range(16)))
for row in range(2, 8):
    cells = []
    for col in range(16):
        code = 16 * row + col
        cells.append(chr(code) if code < 127 else ".")
    print(f"{row:X}x   " + " ".join(cells))
