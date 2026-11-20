total = 0
number = int(input("Number (0 to stop): "))
while number != 0:
    total = total + number
    number = int(input("Number (0 to stop): "))
print("Total:", total)
