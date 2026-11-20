MOVES = {"w": [-1, 0], "s": [1, 0], "a": [0, -1], "d": [0, 1]}


def check_level(text):
    """An empty string if the level is right, or what is wrong with it."""
    rows = text.splitlines()[1:]
    for row in rows:
        if len(row) != len(rows[0]):
            return "every row must have the same length"
    if text.count("S") != 1 or text.count("T") != 1:
        return "a level needs exactly one S and one T"
    return ""


def parse_level(text):
    """The state of a game, from the text of a checked level file."""
    lines = text.splitlines()
    grid = []
    for r in range(1, len(lines)):
        grid.append(list(lines[r]))
        if "S" in lines[r]:
            start = [r - 1, lines[r].index("S")]
    grid[start[0]][start[1]] = "."
    return {"grid": grid, "row": start[0], "col": start[1],
            "gems_left": text.count("g"), "moves_left": int(lines[0])}


def read_text(filename):
    with open(filename, encoding="utf-8") as f:
        return f.read()


def draw(state):
    for r in range(len(state["grid"])):
        line = ""
        for c in range(len(state["grid"][r])):
            if r == state["row"] and c == state["col"]:
                line = line + "@"
            else:
                line = line + state["grid"][r][c]
        print(line)
    print("gems left:", state["gems_left"], "  moves left:", state["moves_left"])


def can_move(state, key):
    """True if the player may move in the direction of key."""
    cell = state["grid"][state["row"] + MOVES[key][0]][state["col"] + MOVES[key][1]]
    if cell == "#":
        return False
    if cell == "=" and state["gems_left"] > 0:
        return False
    return True


def move(state, key):
    """Move the player one cell; collect a gem; open the gate after the last."""
    state["row"] = state["row"] + MOVES[key][0]
    state["col"] = state["col"] + MOVES[key][1]
    state["moves_left"] = state["moves_left"] - 1
    grid = state["grid"]
    if grid[state["row"]][state["col"]] == "g":
        grid[state["row"]][state["col"]] = "."
        state["gems_left"] = state["gems_left"] - 1
        if state["gems_left"] == 0:
            for row in grid:
                for c in range(len(row)):
                    if row[c] == "=":
                        row[c] = "."


def won(state):
    return state["grid"][state["row"]][state["col"]] == "T"


if __name__ == "__main__":
    state = parse_level(read_text("level1.txt"))
    for key in "wssss":
        if can_move(state, key):
            move(state, key)
            print(key, "-> row", state["row"], "column", state["col"],
                  " gems left:", state["gems_left"])
        else:
            print(key, "-> blocked")
    draw(state)
