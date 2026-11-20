# The ages on each side of the two boundaries, 12 and 65.
for age in [11, 12, 64, 65]:
    if age < 12:
        price = 5
    elif age < 65:
        price = 9
    else:
        price = 6
    print(age, price)
