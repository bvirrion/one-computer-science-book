"""skyline.py: the outline of buildings (left, right, height) seen from afar,
as a list of (x, height) points where the height changes."""


def skyline(buildings):
    if not buildings:
        return []
    if len(buildings) == 1:
        left, right, h = buildings[0]
        return [(left, h), (right, 0)]
    mid = len(buildings) // 2
    return merge(skyline(buildings[:mid]), skyline(buildings[mid:]))


def merge(a, b):
    """Merge two outlines: at each x, the higher of the two current heights."""
    out, i, j, ha, hb = [], 0, 0, 0, 0
    while i < len(a) or j < len(b):
        xa = a[i][0] if i < len(a) else float("inf")
        x = min(xa, b[j][0] if j < len(b) else float("inf"))
        if i < len(a) and a[i][0] == x:
            ha = a[i][1]
            i += 1
        if j < len(b) and b[j][0] == x:
            hb = b[j][1]
            j += 1
        h = max(ha, hb)
        if not out or out[-1][1] != h:
            out.append((x, h))
    return out
