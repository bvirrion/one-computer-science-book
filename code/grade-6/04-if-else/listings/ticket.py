age = int(input("Age: "))
if age < 12:
    price = 5
elif age < 65:
    price = 9
else:
    price = 6
print(f"Ticket: {price} euros")
