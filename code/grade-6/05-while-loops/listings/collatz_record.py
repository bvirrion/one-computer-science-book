# Which start below 100 takes the most steps to reach 1?
best_start = 1
best_steps = 0
for start in range(1, 100):
    n = start
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps = steps + 1
    if steps > best_steps:
        best_start = start
        best_steps = steps
print("start:", best_start, "steps:", best_steps)
