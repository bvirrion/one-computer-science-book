DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def to_base(n, b):
    """Return the digits of the whole number n >= 0 in base b, 2 <= b <= 36."""
    if n == 0:
        return "0"
    digits = ""
    while n > 0:
        digits = DIGITS[n % b] + digits
        n = n // b
    return digits


for b in (2, 8, 10, 16, 36):
    print(f"2026 in base {b:2}: {to_base(2026, b)}")
print(int("11111101010", 2), int("7EA", 16))
