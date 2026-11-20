"""exo_negative.py: exercise 6, subset-sum pruning on values that may be negative."""


def count(values, target, prune):
    found = []

    def visit(i, chosen, total):
        if prune and total > target:
            return  # "too much already"
        if i == len(values):
            if total == target:
                found.append(chosen)
            return
        visit(i + 1, chosen + [values[i]], total + values[i])
        visit(i + 1, chosen, total)

    visit(0, [], 0)
    return found


if __name__ == "__main__":
    values = [8, 5, -4, 3, -2]
    print("without pruning:", count(values, 6, prune=False))
    print("with pruning:   ", count(values, 6, prune=True))
