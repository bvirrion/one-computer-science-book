from load_weather import read_table

weather = read_table("weather.csv")

# selection: keep the records that satisfy a condition
wet = [row for row in weather if row["station"] == "Hilltop" and row["rain_mm"] >= 15]
# projection: keep some columns of each record
print([(row["date"], row["rain_mm"]) for row in wet])
print(len(weather), "->", len(wet), "records;", len(weather[0]), "-> 2 columns")
