def rotate_copy(grid):
    """A quarter turn clockwise, into a new grid: the row r becomes column n-1-r."""
    n = len(grid)
    out = [[None] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            out[c][n - 1 - r] = grid[r][c]
    return out


def show(grid):
    for row in grid:
        print(" ".join(f"{x:>2}" for x in row))


if __name__ == "__main__":
    g = [[4 * r + c for c in range(4)] for r in range(4)]
    show(g)
    print("--- a quarter turn clockwise:")
    show(rotate_copy(g))
