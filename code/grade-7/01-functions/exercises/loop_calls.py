def square(n):
    print("computing", n)
    return n * n


total = 0
for i in range(1, 5):
    total = total + square(i)
print(total)
