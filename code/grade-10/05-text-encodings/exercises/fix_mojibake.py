"""Exercise 14: undo one layer of UTF-8 bytes read as Latin-1."""


def fix_mojibake(s):
    """Return s re-read as UTF-8 if it is UTF-8 read as Latin-1, else s itself."""
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s
