def step(grid):
    """One generation: a living cell (1) lives on with 2 or 3 living neighbours;
    an empty cell (0) comes to life with exactly 3."""
    new = []
    for r in range(len(grid)):
        row = []
        for c in range(len(grid[0])):
            alive = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr = r + dr
                    nc = c + dc
                    inside = 0 <= nr < len(grid) and 0 <= nc < len(grid[0])
                    if (dr != 0 or dc != 0) and inside:
                        alive = alive + grid[nr][nc]
            if grid[r][c] == 1 and alive in [2, 3]:
                row.append(1)
            elif grid[r][c] == 0 and alive == 3:
                row.append(1)
            else:
                row.append(0)
        new.append(row)
    return new
