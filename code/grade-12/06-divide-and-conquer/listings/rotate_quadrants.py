from rotate_copy import rotate_copy, show


def rotate_in_place(grid, top=0, left=0, size=None):
    """Rotate the square block of a 2^k grid a quarter turn clockwise, in place."""
    if size is None:
        size = len(grid)
    if size == 1:
        return
    h = size // 2
    for r in range(h):                       # move the four quadrants round:
        for c in range(h):                   # top-left -> top-right -> bottom-right
            a = (top + r, left + c)          # -> bottom-left -> top-left
            b = (top + r, left + h + c)
            d = (top + h + r, left + h + c)
            e = (top + h + r, left + c)
            t = grid[e[0]][e[1]]
            grid[e[0]][e[1]] = grid[d[0]][d[1]]
            grid[d[0]][d[1]] = grid[b[0]][b[1]]
            grid[b[0]][b[1]] = grid[a[0]][a[1]]
            grid[a[0]][a[1]] = t
    for dr, dc in [(0, 0), (0, h), (h, 0), (h, h)]:
        rotate_in_place(grid, top + dr, left + dc, h)   # then turn each quadrant


if __name__ == "__main__":
    g = [[4 * r + c for c in range(4)] for r in range(4)]
    expected = rotate_copy(g)
    rotate_in_place(g)
    show(g)
    print("same as the copy:", g == expected)
