rows = ["#########",
        "#S..#.#T#",
        "#.#.#.#=#",
        "#g#...#.#",
        "#.###g#.#",
        "#.......#",
        "#########"]
grid = []
for row in rows:
    grid.append(list(row))           # a list of characters per row
grid[1][1] = "."                     # the player stands on the floor
state = {"grid": grid, "row": 1, "col": 1, "gems_left": 2, "moves_left": 20}

print("the maze has", len(grid), "rows and", len(grid[0]), "columns")
print("the player is at row", state["row"], "column", state["col"])
print("below the player:", repr(grid[state["row"] + 1][state["col"]]))
print("right of the start:", repr(grid[1][2]), " the treasure:", repr(grid[1][7]))
print("gems left:", state["gems_left"], " moves left:", state["moves_left"])
