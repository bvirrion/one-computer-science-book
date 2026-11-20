n = 44
remainders = []
while n > 0:
    print(n, "= 2 x", n // 2, "+", n % 2)
    remainders.append(n % 2)
    n = n // 2

bits = ""
for r in remainders:
    bits = str(r) + bits          # the last remainder ends up first
print("binary:", bits)
