from maze_v5 import MOVES, play

MOVES["x"] = [0, 0]          # x: stay in place, and spend a move

if __name__ == "__main__":
    play("level1.txt")
