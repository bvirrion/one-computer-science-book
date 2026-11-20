from date_class import Date

for d in [Date(2026, 3, 14), Date(2028, 2, 28), Date(2027, 2, 28), Date(2026, 12, 31)]:
    print(d, "->", d.next_day())
print(Date(2026, 1, 31) < Date(2026, 2, 1), Date(2026, 5, 1) == Date(2026, 5, 1))
for bad in [(2027, 2, 29), (2026, 13, 1), (2026, 4, 31)]:
    try:
        Date(*bad)
    except ValueError as error:
        print("ValueError:", error)
