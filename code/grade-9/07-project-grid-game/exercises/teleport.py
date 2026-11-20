from maze_v5 import move


def move_teleport(state, key):
    """Move as usual; a player who lands on an o jumps to the other o."""
    move(state, key)
    grid = state["grid"]
    if grid[state["row"]][state["col"]] == "o":
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] == "o" and [r, c] != [state["row"], state["col"]]:
                    target = [r, c]
        state["row"] = target[0]
        state["col"] = target[1]
