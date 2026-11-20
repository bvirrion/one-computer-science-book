def neighbours4(grid, r, c):
    """The values above, below, left and right of grid[r][c], inside the grid."""
    found = []
    for place in [[r - 1, c], [r + 1, c], [r, c - 1], [r, c + 1]]:
        nr = place[0]
        nc = place[1]
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            found.append(grid[nr][nc])
    return found
