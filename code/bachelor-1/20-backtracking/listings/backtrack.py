"""backtrack.py: the generic method, as a function of the problem's three parts."""


def backtrack(partial, choices, is_valid, is_complete, found):
    """Extend `partial` in every way that stays valid; report every complete one."""
    if is_complete(partial):
        found(list(partial))
        return
    for c in choices(partial):
        partial.append(c)
        if is_valid(partial):  # prune: no completion of an invalid partial solution
            backtrack(partial, choices, is_valid, is_complete, found)
        partial.pop()  # undo the choice


if __name__ == "__main__":
    # the words of 3 letters over "ab" with no two equal neighbours
    words = []
    backtrack([], lambda p: "ab", lambda p: len(p) < 2 or p[-1] != p[-2],
              lambda p: len(p) == 3, lambda w: words.append("".join(w)))
    print(words)
