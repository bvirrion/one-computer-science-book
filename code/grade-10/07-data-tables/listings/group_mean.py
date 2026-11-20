from load_weather import read_table

weather = read_table("weather.csv")
groups = {}  # (station, month) -> list of temperatures
for row in weather:
    if row["temp_c"] is not None:
        key = (row["station"], row["date"][5:7])
        groups.setdefault(key, []).append(row["temp_c"])

print("month  Hilltop  Riverside")
for month in ["01", "02", "06", "07", "12"]:
    means = [sum(groups[s, month]) / len(groups[s, month])
             for s in ("Hilltop", "Riverside")]
    print(f"{month:5} {means[0]:8.2f} {means[1]:10.2f}")
