def price(age):
    if age < 12:
        return 5
    elif age < 65:
        return 9
    else:
        return 6


for age in [11, 12, 64, 65]:
    print(age, price(age))
