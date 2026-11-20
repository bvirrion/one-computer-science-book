from load_weather import read_table

weather = read_table("weather.csv")
windy = sorted(weather, key=lambda row: row["wind_kmh"], reverse=True)
for row in windy[:4]:
    print(row["date"], row["station"], row["wind_kmh"])

june = [row for row in weather if row["date"].startswith("2025-06-1")]
by_station_then_rain = sorted(june, key=lambda row: (row["station"], -row["rain_mm"]))
for row in by_station_then_rain[:4]:
    print(row["station"], row["date"], row["rain_mm"])
