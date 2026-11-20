n = int(input("A whole number: "))
total = 0
while n > 0:
    total = total + n % 10     # the last digit
    n = n // 10                # remove it
print("Sum of the digits:", total)
