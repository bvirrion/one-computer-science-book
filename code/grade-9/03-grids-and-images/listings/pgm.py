def read_pgm(filename):
    """The grey levels of a plain PGM file, as a grid of whole numbers."""
    with open(filename, encoding="utf-8") as f:
        words = f.read().split()
    width = int(words[1])
    height = int(words[2])
    values = words[4:]                   # after P2, width, height and 255
    grid = []
    for r in range(height):
        row = []
        for c in range(width):
            row.append(int(values[r * width + c]))
        grid.append(row)
    return grid


def pgm_text(grid):
    """The text of a plain PGM file holding the grid."""
    lines = ["P2", str(len(grid[0])) + " " + str(len(grid)), "255"]
    for row in grid:
        line = ""
        for value in row:
            line = line + f"{value:>4}"
        lines.append(line)
    return "\n".join(lines)
