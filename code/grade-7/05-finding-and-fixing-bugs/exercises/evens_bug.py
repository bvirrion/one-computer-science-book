n = 10
total = 0
for i in range(1, n):
    if i % 2 == 1:
        total = total + i
print("sum of the even numbers up to", n, ":", total)
