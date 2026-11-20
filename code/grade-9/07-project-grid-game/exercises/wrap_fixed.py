MOVES = {"w": [-1, 0], "s": [1, 0], "a": [0, -1], "d": [0, 1]}
grid = [list("S.g"), list(".#."), list("..T")]


def can_move(row, col, key):
    r = row + MOVES[key][0]
    c = col + MOVES[key][1]
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return False                     # off the edge of the maze
    return grid[r][c] != "#"


print(can_move(0, 0, "a"), can_move(0, 0, "w"), can_move(1, 0, "d"))
