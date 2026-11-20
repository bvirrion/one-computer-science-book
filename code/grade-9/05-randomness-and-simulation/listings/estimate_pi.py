import random


def points_inside(n):
    """Throw n points in the 1 by 1 square; count those in the quarter disc."""
    inside = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1:
            inside = inside + 1
    return inside


if __name__ == "__main__":
    random.seed(8)
    for n in [100, 10_000, 1_000_000]:
        inside = points_inside(n)
        print(f"{n:>9} points: {inside:>7} inside, pi is about {4 * inside / n:.4f}")
