def draw_fog(state, sight):
    """Draw only the cells at most sight rows and columns from the player."""
    for r in range(len(state["grid"])):
        line = ""
        for c in range(len(state["grid"][r])):
            if r == state["row"] and c == state["col"]:
                line = line + "@"
            elif abs(r - state["row"]) <= sight and abs(c - state["col"]) <= sight:
                line = line + state["grid"][r][c]
            else:
                line = line + "?"
        print(line)
