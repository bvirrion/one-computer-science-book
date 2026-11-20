import random


def walk(steps):
    """The positions of a token that moves 1 left or 1 right at each step."""
    position = 0
    path = [0]
    for _ in range(steps):
        if random.random() < 0.5:
            position = position + 1
        else:
            position = position - 1
        path.append(position)
    return path


if __name__ == "__main__":
    random.seed(11)
    path = walk(100)
    print("positions at steps 0 to 10:", path[:11])
    print("end:", path[-1])
    print("farthest right:", max(path), " farthest left:", min(path))
