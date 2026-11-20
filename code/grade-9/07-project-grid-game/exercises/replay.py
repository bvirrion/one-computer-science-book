from maze_v5 import can_move, move, parse_level, read_text, won


def replay(text, sequence):
    """The number of moves used to win with sequence, or -1 if it does not win."""
    state = parse_level(text)
    used = 0
    for key in sequence:
        if state["moves_left"] > 0 and can_move(state, key):
            move(state, key)
            used = used + 1
            if won(state):
                return used
    return -1


if __name__ == "__main__":
    print(replay(read_text("level1.txt"), "wssssddddwsddwwww"))
    print(replay(read_text("level1.txt"), "ssss"))
