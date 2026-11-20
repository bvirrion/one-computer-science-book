"""Change with the fewest coins, for any coin system."""


def change_table(amount, coins):
    """best[a]: fewest coins for a; last[a]: one coin of a best way."""
    best = [0] + [None] * amount
    last = [None] * (amount + 1)
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and best[a - c] is not None:
                if best[a] is None or best[a - c] + 1 < best[a]:
                    best[a] = best[a - c] + 1
                    last[a] = c
    return best, last


def rebuild(amount, last):
    used = []
    while amount > 0:                   # follow the recorded choices back
        used.append(last[amount])
        amount -= last[amount]
    return used


if __name__ == "__main__":
    best, last = change_table(6, [1, 3, 4])
    print("amount:", list(range(7)))
    print("best:  ", best)
    print("last:  ", last)
    print("6 =", rebuild(6, last), "  greedy gave [4, 1, 1]")
    best, last = change_table(36, [1, 2, 5, 12, 25, 40])
    print("Brenmoor, 36 =", rebuild(36, last), "  greedy gave [25, 5, 5, 1]")
