from rain import rain

longest = 0
longest_end = 0
run = 0                          # dry days in a row, up to today
for i in range(len(rain)):
    if rain[i] == 0:
        run = run + 1
        if run > longest:
            longest = run
            longest_end = i
    else:
        run = 0
start = longest_end - longest + 1
print("longest dry run:", longest, "days, from January", start + 1)
