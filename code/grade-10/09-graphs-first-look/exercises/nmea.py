"""Exercise 11: the position in a GGA sentence, in decimal degrees, and its checksum."""
from functools import reduce


def checksum(sentence):
    """XOR of the characters between $ and *, as two hexadecimal digits."""
    body = sentence[1:sentence.index("*")]
    return f"{reduce(lambda x, c: x ^ ord(c), body, 0):02X}"


def to_degrees(value, hemisphere, degree_digits):
    """ddmm.mmmm (or dddmm.mmmm) to signed decimal degrees."""
    degrees = int(value[:degree_digits])
    minutes = float(value[degree_digits:])
    sign = -1 if hemisphere in "SW" else 1
    return sign * (degrees + minutes / 60)


def position(sentence):
    fields = sentence.split(",")
    return to_degrees(fields[2], fields[3], 2), to_degrees(fields[4], fields[5], 3)
