from maze_v5 import read_text
from try_all_moves import all_sequences, wins


def shortest(text, most):
    """The first winning sequence, trying the lengths 1, 2, 3, ... in order."""
    for n in range(1, most + 1):
        for sequence in all_sequences(n):
            if wins(text, sequence):
                return sequence
    return ""


if __name__ == "__main__":
    print(shortest(read_text("tiny.txt"), 7))
