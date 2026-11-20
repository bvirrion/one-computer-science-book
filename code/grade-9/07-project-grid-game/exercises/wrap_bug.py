MOVES = {"w": [-1, 0], "s": [1, 0], "a": [0, -1], "d": [0, 1]}
grid = [list("S.g"), list(".#."), list("..T")]


def can_move(row, col, key):
    cell = grid[row + MOVES[key][0]][col + MOVES[key][1]]
    return cell != "#"


print(can_move(0, 0, "a"), can_move(0, 0, "w"), can_move(1, 0, "d"))
