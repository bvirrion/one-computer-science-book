def add_unsigned(a, b, n):
    """Add a and b as an n-bit unsigned adder does: keep the n lowest bits."""
    return (a + b) % 2**n


counter = 0
for step in range(65_540):
    counter = add_unsigned(counter, 1, 16)
    if step >= 65_533:
        print("after", step + 1, "steps the counter shows", counter)

print("8 bits:  250 + 10 =", add_unsigned(250, 10, 8))
print("16 bits: 250 + 10 =", add_unsigned(250, 10, 16))
