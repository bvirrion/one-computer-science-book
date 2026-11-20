trap = [[0] * 3] * 3
trap[0][0] = 1
print(trap)

safe = []
for _ in range(3):
    safe.append([0] * 3)
safe[0][0] = 1
print(safe)
