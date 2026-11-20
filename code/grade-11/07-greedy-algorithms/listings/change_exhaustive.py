"""The fewest coins by trying every combination: slow, but surely right."""
from change_greedy import greedy_change


def fewest(amount, coins):
    """Return (fewest coins, combinations tried). coins sorted, coins[0] == 1."""
    if len(coins) == 1:
        return amount, 1                  # only coins of 1 left
    *smaller, c = coins
    best, tried = None, 0
    for k in range(amount // c + 1):      # k coins of the largest value, then the rest
        n, t = fewest(amount - k * c, smaller)
        tried += t
        if best is None or k + n < best:
            best = k + n
    return best, tried


if __name__ == "__main__":
    print("20 with 1, 2, 5:", fewest(20, [1, 2, 5]))
    coins = [1, 2, 5, 10, 20, 50]
    limit = coins[-1] + coins[-2]         # 70: the theorem says this is far enough
    bad = [a for a in range(1, limit)
           if len(greedy_change(a, coins)) != fewest(a, coins)[0]]
    print(f"amounts below {limit} where greedy is not optimal: {bad}")
