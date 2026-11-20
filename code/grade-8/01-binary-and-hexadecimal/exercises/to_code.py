DIGITS = "0123456789ABCDEF"


def two_hex(n):
    """A number from 0 to 255 as two hexadecimal digits."""
    return DIGITS[n // 16] + DIGITS[n % 16]


def colour_code(red, green, blue):
    return "#" + two_hex(red) + two_hex(green) + two_hex(blue)


print(colour_code(255, 136, 0), colour_code(46, 139, 87), colour_code(0, 0, 0))
