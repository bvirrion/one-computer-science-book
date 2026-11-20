patterns = []
for a in "01":
    for b in "01":
        for c in "01":
            patterns.append(a + b + c)
print(len(patterns), "patterns of 3 bits:", patterns)

count = 1                          # 0 bits: one pattern, the empty one
for n in range(1, 11):
    count = count * 2              # one more bit: each pattern gets a 0 or a 1
    print("n =", n, ":", count, "patterns, largest number", count - 1)
