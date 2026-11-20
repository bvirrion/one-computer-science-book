"""edit_two_rows.py: the edit distance with two rows of the table, not all of it."""

from edit_distance import table


def distance(a, b):
    previous = list(range(len(b) + 1))  # row 0 of the table
    for i in range(1, len(a) + 1):
        current = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            current[j] = min(previous[j] + 1, current[j - 1] + 1,
                             previous[j - 1] + (a[i - 1] != b[j - 1]))
        previous = current  # row i - 1 is no longer needed
    return previous[-1]


def main():
    a = "a spelling checker for the catalogue"
    b = "a speling chekcer for teh catalog"
    full = table(a, b)
    print(f"distance {distance(a, b)} (full table: {full[-1][-1]})")
    print(f"cells kept: full table {(len(a) + 1) * (len(b) + 1)},"
          f" two rows {2 * (len(b) + 1)}")


if __name__ == "__main__":
    main()
