from rain import rain

total = 0
for amount in rain:
    total = total + amount
print("average:", round(total / len(rain), 2), "mm a day")
