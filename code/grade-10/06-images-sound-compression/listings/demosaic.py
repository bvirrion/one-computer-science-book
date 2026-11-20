# Each photosite measured one colour: R, G or B, in the pattern RG / GB.
MOSAIC = [[200, 120, 190, 118],
          [110, 60, 115, 64],
          [180, 125, 170, 130],
          [105, 58, 100, 62]]


def colour_of(r, c):
    if r % 2 == 0:
        return "R" if c % 2 == 0 else "G"
    return "G" if c % 2 == 0 else "B"


def average(values):
    return round(sum(values) / len(values))


def rgb_at(r, c):
    """(R, G, B) of photosite (r, c): its own value, its neighbours' averages."""
    found = {"R": [], "G": [], "B": []}
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            rr, cc = r + dr, c + dc
            if 0 <= rr < 4 and 0 <= cc < 4 and (dr, dc) != (0, 0):
                found[colour_of(rr, cc)].append(MOSAIC[rr][cc])
    found[colour_of(r, c)] = [MOSAIC[r][c]]
    return tuple(average(found[k]) for k in "RGB")


for r in range(4):
    print("  ".join(f"{colour_of(r, c)}{MOSAIC[r][c]:>3}" for c in range(4)))
print("pixel (1, 1):", rgb_at(1, 1))
print("pixel (2, 2):", rgb_at(2, 2))
