def greedy_change(amount, coins):
    """Take the largest coin that fits, again and again. coins must contain 1."""
    given = []
    for c in sorted(coins, reverse=True):
        while c <= amount:
            given.append(c)
            amount -= c
    return given


if __name__ == "__main__":
    COINS = [1, 2, 5, 10, 20, 50]
    for amount in [87, 43, 9]:
        change = greedy_change(amount, COINS)
        print(f"{amount}: {change} -> {len(change)} coins")
