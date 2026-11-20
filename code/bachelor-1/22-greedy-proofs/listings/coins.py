"""coins.py: change with the fewest coins: largest coin first, against the optimum."""


def greedy_change(amount, coins):
    used = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            amount -= c
            used.append(c)
    return used


def fewest_coins(amount, coins):
    """The fewest coins for every amount up to `amount`, smallest amounts first."""
    best = [0] + [None] * amount
    for a in range(1, amount + 1):
        options = [best[a - c] for c in coins if c <= a and best[a - c] is not None]
        best[a] = min(options) + 1 if options else None
    return best


def main():
    for coins in ([1, 2, 5, 10, 20, 50, 100, 200], [1, 3, 4], [1, 5, 10, 12]):
        best = fewest_coins(300, coins)
        bad = [a for a in range(1, 301) if len(greedy_change(a, coins)) != best[a]]
        print(f"coins {coins}: greedy worse for {len(bad)} amounts up to 300")
        if bad:
            a = bad[0]
            print(f"  first: {a} = {' + '.join(map(str, greedy_change(a, coins)))}"
                  f" by greedy, {best[a]} coins at best")

if __name__ == "__main__":
    main()
