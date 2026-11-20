"""Exercise 8: the histogram of the grey levels of a plain PGM (P2) image."""


def histogram(text):
    """Return a list h of maxval + 1 counts: h[v] pixels have the grey level v."""
    words = text.split()
    assert words[0] == "P2", "not a plain PGM image"
    width, height, maxval = int(words[1]), int(words[2]), int(words[3])
    values = [int(w) for w in words[4:4 + width * height]]
    h = [0] * (maxval + 1)
    for v in values:
        h[v] += 1
    return h
