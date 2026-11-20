DIGITS = "0123456789ABCDEF"


def to_number(text, base):
    value = 0
    for ch in text.upper():
        value = value * base + DIGITS.find(ch)
    return value


def from_number(n, base):
    if n == 0:
        return "0"
    text = ""
    while n > 0:
        text = DIGITS[n % base] + text
        n = n // base
    return text


def convert(text, from_base, to_base):
    return from_number(to_number(text, from_base), to_base)


print(convert("101100", 2, 16), convert("FF", 16, 2))
print(convert("255", 10, 8), convert("777", 8, 3))
