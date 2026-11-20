def move(state, key):
    state["row"] = state["row"] + MOVES[key][0]
    state["col"] = state["col"] + MOVES[key][1]
    state["moves_left"] = state["moves_left"] - 1
    grid = state["grid"]
    if grid[state["row"]][state["col"]] == "g":
        grid[state["row"]][state["col"]] = "."
        state["gems_left"] = state["gems_left"] - 1
    if state["gems_left"] <= 1:
        for row in grid:
            for c in range(len(row)):
                if row[c] == "=":
                    row[c] = "."


MOVES = {"w": [-1, 0], "s": [1, 0], "a": [0, -1], "d": [0, 1]}
