import csv

with open("weather.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

missing = 0
codes = 0
all_values = []
good_values = []
dates = []
twice = []
for row in rows:
    if row["station"] == "Riverside":
        if row["date"] in dates:
            twice.append(row["date"])
        dates.append(row["date"])
        if row["temp_c"] == "":
            missing = missing + 1
        else:
            value = float(row["temp_c"])
            all_values.append(value)
            if value == -99.0:
                codes = codes + 1
            else:
                good_values.append(value)

print("Riverside:", len(dates), "rows,", missing, "missing,", codes, "codes")
print("dates seen twice:", twice)
print("mean with the codes:   ", round(sum(all_values) / len(all_values), 2))
print("mean without the codes:", round(sum(good_values) / len(good_values), 2))
