"""fairness.py: two AIMD flows share a link of capacity C; Jain's index."""


def jain(xs):
    return sum(xs) ** 2 / (len(xs) * sum(x * x for x in xs))


def trajectory(x1, x2, capacity, n, increase=1.0, decrease=0.5):
    for _ in range(n):
        yield x1, x2
        if x1 + x2 > capacity:                   # both see the loss: both decrease
            x1, x2 = x1 * decrease, x2 * decrease
        else:                                    # both add the same amount
            x1, x2 = x1 + increase, x2 + increase


if __name__ == "__main__":
    print("round      x1      x2   index")
    for r, (x1, x2) in enumerate(trajectory(4.0, 40.0, 50.0, 201)):
        if r % 25 == 0:
            print(f"{r:5} {x1:7.2f} {x2:7.2f} {jain([x1, x2]):7.4f}")
