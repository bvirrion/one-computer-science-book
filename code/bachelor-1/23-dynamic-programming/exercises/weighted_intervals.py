"""weighted_intervals.py: compatible talks [start, end) of largest total weight."""

from bisect import bisect_right


def best_weight(talks):
    """talks: (start, end, weight). best[i]: the best of the first i talks by end."""
    talks = sorted(talks, key=lambda t: t[1])
    ends = [t[1] for t in talks]
    best = [0] * (len(talks) + 1)
    for i, (s, _, w) in enumerate(talks, start=1):
        p = bisect_right(ends, s, 0, i - 1)  # talks ending at or before s
        best[i] = max(best[i - 1], best[p] + w)  # without talk i, or with it
    return best[-1]
