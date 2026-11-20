from ballots import BALLOTS, CANDIDATES


def count_per_candidate(ballots, candidates):
    """For each candidate, walk all the ballots. Also count the names looked at."""
    results = []
    looked_at = 0
    for name in candidates:
        votes = 0
        for ballot in ballots:
            looked_at = looked_at + 1
            if ballot == name:
                votes = votes + 1
        results.append(votes)
    return results, looked_at


if __name__ == "__main__":
    results, looked_at = count_per_candidate(BALLOTS, CANDIDATES)
    for i in range(len(CANDIDATES)):
        print(CANDIDATES[i], results[i])
    print("names looked at:", looked_at)
