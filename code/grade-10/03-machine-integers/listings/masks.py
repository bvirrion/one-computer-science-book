flags = 0b1010_0110

print(format(flags, "08b"), "bit 2 is", (flags >> 2) & 1)
print(format(flags | (1 << 0), "08b"), "after setting bit 0")
print(format(flags & ~(1 << 5), "08b"), "after clearing bit 5")
print(format(flags ^ 0b1111_1111, "08b"), "after flipping every bit")

colour = 0xF4A261  # a sandy orange, as on a web page
red = (colour >> 16) & 0xFF
green = (colour >> 8) & 0xFF
blue = colour & 0xFF
print("red", red, "green", green, "blue", blue)
print(hex((red << 16) | (green << 8) | blue))
