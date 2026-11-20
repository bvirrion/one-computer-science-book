"""The Boyer-Moore-Horspool search."""
from shift_table import shift_table


def horspool(text, p, trace=False):
    n, m = len(text), len(p)
    shift = shift_table(p)
    positions, comparisons, i = [], 0, 0
    while i <= n - m:                       # p is under text[i:i + m]
        j = m - 1
        while j >= 0:                       # compare from the right
            comparisons += 1
            if text[i + j] != p[j]:
                break
            j -= 1
        if j < 0:
            positions.append(i)
        last = text[i + m - 1]              # the text letter under p's last place
        if trace:
            print(f"{' ' * i}{p}   at {i:2}: {'found' if j < 0 else 'no'},"
                  f" '{last}' -> jump {shift.get(last, m)}")
        i += shift.get(last, m)
    return positions, comparisons


if __name__ == "__main__":
    text = "the bus to the station stops at the town hall"
    print(text)
    print(horspool(text, "station", trace=True))
    print(horspool(text, "the"))
