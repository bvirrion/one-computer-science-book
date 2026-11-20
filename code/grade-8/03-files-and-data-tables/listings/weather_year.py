import csv

with open("weather.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

rain = {}
warm = 0
for row in rows:
    if row["station"] == "Hilltop":
        month = row["date"][5:7]
        rain[month] = rain.get(month, 0) + float(row["rain_mm"])
        if row["temp_c"] != "" and float(row["temp_c"]) > 20:
            warm = warm + 1

wettest = "01"
for month in rain:
    print(month, round(rain[month], 1), "mm")
    if rain[month] > rain[wettest]:
        wettest = month
print("wettest month:", wettest, "with", round(rain[wettest], 1), "mm")
print("days above 20 degrees:", warm)
