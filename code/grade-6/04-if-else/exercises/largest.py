a = float(input("First: "))
b = float(input("Second: "))
c = float(input("Third: "))
largest = a
if b > largest:
    largest = b
if c > largest:
    largest = c
print("The largest is", largest)
