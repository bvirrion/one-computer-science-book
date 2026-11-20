grid = [[3, 8, 1, 6],
        [7, 2, 9, 4],
        [5, 0, 4, 2]]
print("rows:", len(grid), " columns:", len(grid[0]))
print("grid[1][2] =", grid[1][2])
grid[1][2] = 0
print("row 1 is now", grid[1])

zeros = []
for _ in range(2):
    row = []
    for _ in range(3):
        row.append(0)
    zeros.append(row)
print(zeros)
