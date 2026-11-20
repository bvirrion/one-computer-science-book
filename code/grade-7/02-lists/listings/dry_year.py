from hilltop_2025 import month_days, rain

names = ["January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"]


def date(day):
    """Day 0 of the year is 1 January; give the month and the day of the month."""
    month = 0
    while day >= month_days[month]:
        day = day - month_days[month]
        month = month + 1
    return f"{day + 1} {names[month]}"


longest = 0
longest_end = 0
run = 0
for i in range(len(rain)):
    if rain[i] == 0:
        run = run + 1
        if run > longest:
            longest = run
            longest_end = i
    else:
        run = 0
start = longest_end - longest + 1
print("days in 2025:", len(rain))
print("longest dry spell:", longest, "days")
print("from", date(start), "to", date(longest_end))
