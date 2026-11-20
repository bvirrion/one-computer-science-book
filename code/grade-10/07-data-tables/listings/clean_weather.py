from load_weather import read_table

weather = read_table("weather.csv")
missing = [r["date"] + " " + r["station"] for r in weather if r["temp_c"] is None]
codes = [r["date"] + " " + r["station"] for r in weather if r["temp_c"] == -99.0]
seen, duplicates, clean = set(), [], []
for r in weather:
    key = (r["date"], r["station"])
    if key in seen:
        duplicates.append(key)
    elif r["temp_c"] is not None and r["temp_c"] != -99.0:
        clean.append(r)
    seen.add(key)
print("missing:", len(missing), missing[:2])
print("error codes:", codes)
print("duplicates:", duplicates)


def mean_temp(rows, station):
    values = [r["temp_c"] for r in rows
              if r["station"] == station and r["temp_c"] is not None]
    return sum(values) / len(values), len(values)


for station in ("Hilltop", "Riverside"):
    raw, n_raw = mean_temp(weather, station)
    good, n_good = mean_temp(clean, station)
    print(f"{station:9} raw {raw:6.3f} ({n_raw})  clean {good:6.3f} ({n_good})")
