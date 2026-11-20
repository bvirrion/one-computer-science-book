"""Three ways to find whether a list has a duplicate, counting comparisons."""


class Counted:
    """A value that counts every comparison made with < or ==."""
    count = 0

    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        Counted.count += 1
        return self.v < other.v

    def __eq__(self, other):
        Counted.count += 1
        return self.v == other.v


def by_pairs(t):                  # every pair once: i < j
    for i in range(len(t)):
        for j in range(i + 1, len(t)):
            if t[i] == t[j]:
                return True
    return False


def by_sorting(t):                # equal values end up side by side
    s = sorted(t)
    return any(s[k] == s[k + 1] for k in range(len(s) - 1))


def by_set(t):                    # no comparisons counted: hashing instead
    return len(set(t)) < len(t)
