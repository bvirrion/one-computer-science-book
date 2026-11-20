from maze_v5 import read_text
from try_all_moves import all_sequences, wins


def winnable(text, most):
    """True if some sequence of at most most moves wins the level."""
    for n in range(1, most + 1):
        for sequence in all_sequences(n):
            if wins(text, sequence):
                return True
    return False


if __name__ == "__main__":
    print("tiny.txt:", winnable(read_text("tiny.txt"), 6))
    print("level2.txt:", winnable(read_text("level2.txt"), 6))
