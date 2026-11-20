def rainiest_week(rows, station):
    """The first day and the rain of the rainiest 7 days in a row at one station."""
    days = []
    rain = []
    for row in rows:
        if row["station"] == station and row["date"] not in days:
            days.append(row["date"])
            rain.append(float(row["rain_mm"]))
    best = 0
    for start in range(len(rain) - 6):
        if sum(rain[start:start + 7]) > sum(rain[best:best + 7]):
            best = start
    return days[best], round(sum(rain[best:best + 7]), 1)
