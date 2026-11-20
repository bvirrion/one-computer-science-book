"""eight_puzzle.py: the 8-puzzle solved by breadth-first search and by A* with two
heuristics; states expanded."""
import random

from state_space import astar, bfs

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # 0 is the blank, read row by row


def successors(s):
    """Slide a tile into the blank: up to four new states, each of cost 1."""
    b = s.index(0)
    r, c = divmod(b, 3)
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= r + dr < 3 and 0 <= c + dc < 3:
            t = list(s)
            o = 3 * (r + dr) + c + dc
            t[b], t[o] = t[o], t[b]
            yield tuple(t), 1


def misplaced(s):
    return sum(1 for i, x in enumerate(s) if x and x != GOAL[i])


def manhattan(s):
    return sum(abs(i // 3 - (x - 1) // 3) + abs(i % 3 - (x - 1) % 3)
               for i, x in enumerate(s) if x)


def scrambled(moves, rng):
    s = GOAL
    for _ in range(moves):
        s = rng.choice(list(successors(s)))[0]
    return s


if __name__ == "__main__":
    rng = random.Random(3)
    print("moves  BFS expanded  A* misplaced  A* Manhattan")
    for walk in [10, 20, 40, 80, 3000]:
        start = scrambled(walk, rng)
        path, n_bfs = bfs(start, lambda s: s == GOAL, successors)
        _, c1, n_mis = astar(start, lambda s: s == GOAL, successors, misplaced)
        _, c2, n_man = astar(start, lambda s: s == GOAL, successors, manhattan)
        assert len(path) - 1 == c1 == c2
        print(f"{c1:5} {n_bfs:13} {n_mis:13} {n_man:13}")
