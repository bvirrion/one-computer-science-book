grid = [[3, 8, 1, 6],
        [7, 2, 9, 4],
        [5, 0, 4, 2]]
for r in range(len(grid)):
    line = ""
    for c in range(len(grid[r])):
        line = line + f"{grid[r][c]:>3}"
    print(line)
