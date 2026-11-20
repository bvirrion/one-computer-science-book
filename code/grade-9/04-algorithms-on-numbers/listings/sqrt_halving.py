low = 1.0
high = 2.0                     # 1 * 1 < 2 < 2 * 2
for step in range(1, 11):
    middle = (low + high) / 2
    if middle * middle < 2:
        low = middle
    else:
        high = middle
    print(f"{step:>2}: {low:.6f} < root of 2 < {high:.6f}")
