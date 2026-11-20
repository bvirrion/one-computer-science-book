def blur(grid, whole):
    """The 3 x 3 average of every cell (cells outside the grid count as 0)."""
    size = len(grid)
    new = []
    for r in range(size):
        row = []
        for c in range(size):
            total = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if 0 <= r + dr < size and 0 <= c + dc < size:
                        total = total + grid[r + dr][c + dc]
            if whole:
                row.append(round(total / 9))
            else:
                row.append(total / 9)
        new.append(row)
    return new


def lit(grid):
    """The number of cells that are not 0."""
    count = 0
    for row in grid:
        for value in row:
            if value != 0:
                count = count + 1
    return count


for whole in [False, True]:
    grid = []
    for _ in range(15):
        grid.append([0] * 15)
    grid[7][7] = 255                       # one white pixel in the middle
    print("whole grey levels:", whole)
    last_change = 0
    for k in range(1, 21):
        new = blur(grid, whole)
        if new != grid:
            last_change = k
        grid = new
        if k <= 6 or k == 20:
            centre = f"{grid[7][7]:.2f}"
            print(f"  after {k:>2} blurs: {lit(grid):>3} cells lit, centre {centre}")
    print("  the image last changed at blur", last_change)
