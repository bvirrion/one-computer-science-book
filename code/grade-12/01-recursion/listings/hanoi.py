def hanoi(n, start, goal, spare, moves):
    """Append to moves the moves taking n disks from start to goal."""
    if n == 0:
        return
    hanoi(n - 1, start, spare, goal, moves)      # the n - 1 smaller ones out of the way
    moves.append((n, start, goal))               # the largest disk
    hanoi(n - 1, spare, goal, start, moves)      # the n - 1 smaller ones back on top


if __name__ == "__main__":
    moves = []
    hanoi(3, "A", "C", "B", moves)
    for disk, a, b in moves:
        print(f"disk {disk}: {a} -> {b}")
    for n in [1, 2, 3, 4, 5, 10, 15, 20]:
        moves = []
        hanoi(n, "A", "C", "B", moves)
        print(f"n = {n:2}: {len(moves):7} moves, 2**n - 1 = {2**n - 1}")
