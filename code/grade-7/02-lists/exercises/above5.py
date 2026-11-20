from rain import rain

heavy = []
for amount in rain:
    if amount > 5:
        heavy.append(amount)
print(heavy)
