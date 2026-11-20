n = int(input("A whole number: "))
digits = 1
while n >= 10:
    n = n // 10       # remove the last digit
    digits = digits + 1
print("Digits:", digits)
