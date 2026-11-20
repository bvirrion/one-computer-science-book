"""exo_count.py: exercise 1."""

count = 0
for i in range(10):
    for _j in range(i, 10):
        count += 1
print(count)

k, steps = 1, 0
while k < 1000:
    k, steps = 2 * k, steps + 1
print(k, steps)
