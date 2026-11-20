def neighbours(grid, r, c):
    """The values of the up to eight cells around grid[r][c], inside the grid."""
    found = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr = r + dr
            nc = c + dc
            inside = 0 <= nr < len(grid) and 0 <= nc < len(grid[0])
            if (dr != 0 or dc != 0) and inside:
                found.append(grid[nr][nc])
    return found


grid = [[3, 8, 1, 6],
        [7, 2, 9, 4],
        [5, 0, 4, 2]]
print("around grid[1][1]:", neighbours(grid, 1, 1))
print("around grid[0][0]:", neighbours(grid, 0, 0))
big = 0
for value in neighbours(grid, 1, 2):
    if value >= 5:
        big = big + 1
print("neighbours of grid[1][2] that are 5 or more:", big)
