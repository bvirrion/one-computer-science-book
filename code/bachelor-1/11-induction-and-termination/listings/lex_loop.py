"""lex_loop.py: a loop whose variant decreases in the lexicographic order."""

i, j = 3, 0
steps = 0
while i > 0 or j > 0:
    print(f"step {steps:2d}: variant (i, j) = ({i}, {j})")
    if j > 0:
        j -= 1  # (i, j) > (i, j - 1)
    else:
        i, j = i - 1, 2 * i  # (i, 0) > (i - 1, anything): j may grow
    steps += 1
print(f"stopped after {steps} steps at ({i}, {j})")
