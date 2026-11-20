# How many leap years between two years, both included?
count = 0
for year in range(1901, 2101):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        count = count + 1
print("1901 to 2100:", count)

count = 0
for year in range(2001, 2401):
    if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        count = count + 1
print("2001 to 2400:", count)
print("days in 400 years:", 400 * 365 + count)
print("average year:", (400 * 365 + count) / 400)
