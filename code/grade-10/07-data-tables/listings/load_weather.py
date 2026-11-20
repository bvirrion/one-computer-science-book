import csv


def convert(text):
    """Turn a cell into an int, a float, None if empty, or leave it as a string."""
    if text == "":
        return None
    for kind in (int, float):
        try:
            return kind(text)
        except ValueError:
            pass
    return text


def read_table(path):
    """Read a CSV file with a header line into a list of dicts with converted values."""
    with open(path, encoding="utf-8", newline="") as f:
        return [{k: convert(v) for k, v in row.items()} for row in csv.DictReader(f)]


if __name__ == "__main__":
    weather = read_table("weather.csv")
    print(len(weather), "records; columns:", list(weather[0]))
    for row in weather[:2]:
        print(row)
    stations = {}
    for row in weather:
        stations[row["station"]] = stations.get(row["station"], 0) + 1
    print(stations)
