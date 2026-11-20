n = int(input("Start: "))
steps = 0
highest = n
while n != 1:
    if n % 2 == 0:
        n = n // 2
    else:
        n = 3 * n + 1
    steps = steps + 1
    if n > highest:
        highest = n
print("steps:", steps, "highest:", highest)
