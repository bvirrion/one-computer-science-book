import csv

with open("weather.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

total = 0
count = 0
skipped = 0
for row in rows:
    if row["station"] == "Hilltop":
        if row["temp_c"] == "":
            skipped = skipped + 1
        else:
            total = total + float(row["temp_c"])
            count = count + 1
print("Hilltop:", count, "temperatures,", skipped, "missing")
print("mean temperature:", round(total / count, 2), "degrees")
