"""loans_check.py: the hook's answer in Python, to check the pipeline."""

import csv
import sys
from collections import Counter


def top_members(path, k=5):
    with open(path, newline="", encoding="utf8") as f:
        counts = Counter(row["member_id"] for row in csv.DictReader(f))
    # the order of `sort -rn`: by count, then by the whole line, both descending
    ranked = sorted(counts.items(), key=lambda mc: (mc[1], mc[0]), reverse=True)
    return ranked[:k], len(counts)


if __name__ == "__main__":
    top, distinct = top_members(sys.argv[1] if len(sys.argv) > 1 else "loans.csv")
    for member, count in top:
        print(f"{count:7d} {member}")
    print(distinct)
