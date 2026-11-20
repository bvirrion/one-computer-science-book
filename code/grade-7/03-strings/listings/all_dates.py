from dates import date_string, days_in_month, is_palindrome

found = []
for year in range(2001, 2100):
    for month in range(1, 13):
        for day in range(1, days_in_month(month, year) + 1):
            s = date_string(day, month, year)
            if is_palindrome(s):
                found.append(s[0:2] + "-" + s[2:4] + "-" + s[4:])
print(len(found), "palindrome dates")
print("first:", found[0], " last:", found[-1])
for i in range(0, len(found), 5):
    print("  ".join(found[i:i + 5]))
