for age in [8, 30, 70]:
    if age < 65:
        price = 9
    elif age < 12:
        price = 5        # this line can never run
    else:
        price = 6
    print(age, price)
