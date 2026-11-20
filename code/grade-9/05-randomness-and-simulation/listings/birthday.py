import random


def shared(size):
    """Simulate one class: True if two pupils share a birthday."""
    seen = []
    for _ in range(size):
        day = random.randint(1, 365)
        if day in seen:
            return True
        seen.append(day)
    return False


def frequency(size, classes):
    count = 0
    for _ in range(classes):
        if shared(size):
            count = count + 1
    return count / classes


if __name__ == "__main__":
    random.seed(23)
    for size in [5, 10, 15, 20, 23, 25, 30, 40, 50, 60]:
        print(f"{size:>2} pupils: {frequency(size, 10_000):.3f}")
