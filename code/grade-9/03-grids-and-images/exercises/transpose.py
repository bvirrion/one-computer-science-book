def transpose(grid):
    """The grid whose rows are the columns of grid."""
    new = []
    for c in range(len(grid[0])):
        row = []
        for r in range(len(grid)):
            row.append(grid[r][c])
        new.append(row)
    return new
