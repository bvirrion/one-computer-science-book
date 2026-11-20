"""Horspool's shift table: how far may the pattern jump?"""


def shift_table(p):
    """For each letter of p but the last: distance from its last place to the end."""
    m = len(p)
    shift = {}
    for j in range(m - 1):                  # the last letter of p is left out
        shift[p[j]] = m - 1 - j             # later places overwrite earlier ones
    return shift


if __name__ == "__main__":
    for p in ["STATION", "TOWN", "ABAB"]:
        print(p, shift_table(p), "| any other letter:", len(p))
