"""long_division.py: a CRC remainder computed as a written long division."""
from crc import remainder

message, n, g = 0b1101011011, 10, 0b10011       # g(x) = x^4 + x + 1
r = g.bit_length() - 1
value = message << r
width = n + r
print(f"  {value:0{width}b}   message followed by {r} zeros")
for i in range(width - 1, r - 1, -1):
    if value >> i & 1:
        shift = width - 1 - i
        print(" " * (shift + 2) + f"{g:b}" + "   XOR g")
        value ^= g << (i - r)
        print("  " + "-" * width)
        print(f"  {value:0{width}b}")
print(f"remainder: {value:0{r}b}; the frame sent: {message:b} {value:0{r}b}")
assert value == remainder(message, n, g)
