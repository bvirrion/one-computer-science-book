from rain import rain

total = 0
for amount in rain:
    total = total + amount
print("total:", round(total, 1), "mm")

largest = rain[0]
for amount in rain:
    if amount > largest:
        largest = amount
print("wettest day:", largest, "mm")

dry = 0
for amount in rain:
    if amount == 0:
        dry = dry + 1
print("dry days:", dry)
