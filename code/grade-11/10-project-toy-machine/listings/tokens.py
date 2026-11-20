"""Milestone 1: reading the lines of a toy-machine program."""


def parse_number(tok, line):
    """The byte written as decimal, 0x.., 0b.. or 'c'; -128 to -1 wrap to 128-255."""
    tok = tok.strip()
    if len(tok) == 3 and tok[0] == tok[2] == "'":
        value = ord(tok[1])
    else:
        try:
            value = int(tok, 0)
        except ValueError:
            raise ValueError(f"line {line}: {tok!r} is not a number") from None
    if not -128 <= value <= 255:
        raise ValueError(f"line {line}: {value} does not fit in one byte")
    return value % 256


def is_name(tok):
    """True for a name made of letters, digits and _, not starting with a digit."""
    return tok != "" and not tok[0].isdigit() and tok.replace("_", "a").isalnum()


def strip_comment(raw):
    """The line without its comment; a ';' between quotes is a character."""
    kept, quoted = "", False
    for ch in raw:
        if ch == "'":
            quoted = not quoted
        elif ch == ";" and not quoted:
            break
        kept += ch
    return kept


def read_line(raw, line):
    """(label or None, mnemonic or None, operands) for one line of source."""
    code = strip_comment(raw).strip()
    label = None
    head, colon, rest = code.partition(":")
    if colon and is_name(head.strip()):
        label, code = head.strip(), rest.strip()
    if not code:
        return label, None, []
    parts = code.split(None, 1)
    operands = [op.strip() for op in parts[1].split(",")] if len(parts) > 1 else []
    return label, parts[0].upper(), operands


def read_program(text):
    """[(line number, label, mnemonic, operands)] for every line of text."""
    return [(n, *read_line(raw, n)) for n, raw in enumerate(text.splitlines(), start=1)]
