from maze_v5 import can_move, move, parse_level, read_text, won


def wins(text, sequence):
    """True if the moves of sequence reach the treasure (blocked moves are skipped)."""
    state = parse_level(text)
    for key in sequence:
        if state["moves_left"] > 0 and can_move(state, key):
            move(state, key)
            if won(state):
                return True
    return False


def all_sequences(n):
    """Every sequence of n moves: the numbers 0 to 4**n - 1 written in base 4."""
    sequences = []
    for number in range(4 ** n):
        sequence = ""
        for _ in range(n):
            sequence = "wasd"[number % 4] + sequence
            number = number // 4
        sequences.append(sequence)
    return sequences


if __name__ == "__main__":
    for filename in ["tiny.txt", "level2.txt"]:
        text = read_text(filename)
        for n in range(1, 8):
            count = 0
            for sequence in all_sequences(n):
                if wins(text, sequence):
                    count = count + 1
            print(f"{filename:<11} {n} moves: {4 ** n:>6} sequences, {count:>3} win")
