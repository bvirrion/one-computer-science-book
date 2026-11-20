mark = float(input("Mark out of 20: "))
if mark >= 16:
    letter = "A"
elif mark >= 12:
    letter = "B"
elif mark >= 8:
    letter = "C"
else:
    letter = "D"
print("Grade:", letter)
