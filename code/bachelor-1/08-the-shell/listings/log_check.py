"""log_check.py: the busiest hour and the number of distinct members, in Python."""

import re
import sys
from collections import Counter


def check(path):
    with open(path, encoding="utf8") as f:
        lines = f.read().splitlines()
    hours = Counter(line[11:13] for line in lines)
    busiest = max(hours.items(), key=lambda hc: (hc[1], hc[0]))
    members = {m for line in lines for m in re.findall(r"member=([0-9]+)", line)}
    return len(lines), busiest, len(members)


if __name__ == "__main__":
    n, (hour, count), distinct = check(sys.argv[1])
    print(f"{n} lines; busiest hour {hour} with {count} lines;", end=" ")
    print(f"{distinct} distinct members")
