# Every age from 0 to 80, by fives: each branch of the ticket rule is reached.
for age in range(0, 81, 5):
    if age < 12:
        price = 5
    elif age < 65:
        price = 9
    else:
        price = 6
    print(age, price)
