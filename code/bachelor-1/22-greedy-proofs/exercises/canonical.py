"""canonical.py: the canonical prefix code with given codeword lengths: symbols sorted
by (length, symbol), each codeword the previous one plus 1, shifted as lengths grow."""


def canonical(lengths):
    """The codewords, from lengths: symbol -> length (with sum 2^-l <= 1)."""
    code, value, previous = {}, 0, 0
    for s in sorted(lengths, key=lambda s: (lengths[s], s)):
        value <<= lengths[s] - previous  # append zeros up to the new length
        code[s] = format(value, f"0{lengths[s]}b")
        value += 1
        previous = lengths[s]
    return code
