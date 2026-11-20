from rain import rain

best = 0                        # the index of the largest value so far
for i in range(1, len(rain)):
    if rain[i] > rain[best]:
        best = i
print("wettest day: January", best + 1, "with", rain[best], "mm")
