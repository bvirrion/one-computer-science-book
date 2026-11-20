from ballots import BALLOTS


def count_once(ballots):
    """Walk the ballots once, with a dictionary of counts."""
    counts = {}
    looked_at = 0
    for ballot in ballots:
        looked_at = looked_at + 1
        counts[ballot] = counts.get(ballot, 0) + 1
    return counts, looked_at


def winner_and_margin(counts):
    best = ""
    for name in counts:
        if best == "" or counts[name] > counts[best]:
            best = name
    second = 0
    for name in counts:
        if name != best and counts[name] > second:
            second = counts[name]
    return best, counts[best] - second


if __name__ == "__main__":
    counts, looked_at = count_once(BALLOTS)
    print(counts)
    winner, margin = winner_and_margin(counts)
    print("winner:", winner, "by", margin, "votes")
    print("names looked at:", looked_at)
