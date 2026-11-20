"""Exercise 13: run-length coding of a black-and-white bitmap, row by row."""


def rle_row(row):
    runs = []
    for ch in row:
        if runs and runs[-1][1] == ch:
            runs[-1][0] += 1
        else:
            runs.append([1, ch])
    return [tuple(r) for r in runs]


def bitmap_ratio(rows):
    """Return (pixels, runs, ratio), a run costing as much as 2 pixels."""
    pixels = sum(len(r) for r in rows)
    runs = sum(len(rle_row(r)) for r in rows)
    return pixels, runs, pixels / (2 * runs)
