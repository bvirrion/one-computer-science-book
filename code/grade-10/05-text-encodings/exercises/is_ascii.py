"""Exercise 5: is every character of s an ASCII character?"""


def is_ascii(s):
    """Return True when every character of the string s has a code point below 128."""
    for c in s:
        if ord(c) >= 128:
            return False
    return True
