from rain import rain

rainy = 0
for amount in rain:
    if amount > 0:
        rainy = rainy + 1
print("rainy days:", rainy)
