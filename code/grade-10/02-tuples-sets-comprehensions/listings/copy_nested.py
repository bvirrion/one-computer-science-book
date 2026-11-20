import copy

grid = [[0, 0, 0], [0, 0, 0]]
shallow = list(grid)
deep = copy.deepcopy(grid)

shallow[0][0] = 9
deep[1][2] = 7
print("grid:   ", grid)
print("shallow:", shallow)
print("deep:   ", deep)
print(shallow[0] is grid[0], deep[0] is grid[0])
