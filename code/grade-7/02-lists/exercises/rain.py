# Rainfall at Hilltop, January 2025, in millimetres (day 1 first).
rain = [
    0.0, 0.0, 0.7, 0.0, 6.9, 0.0, 0.0, 0.0, 0.0, 3.3,
    0.0, 16.1, 0.0, 0.0, 5.9, 0.0, 3.3, 0.3, 7.7, 0.0,
    0.0, 2.8, 5.4, 0.0, 1.5, 0.0, 0.1, 0.0, 0.0, 2.3,
    0.0,
]
if __name__ == "__main__":
    print("days:", len(rain))
    print("1 January:", rain[0], "mm")
    print("12 January:", rain[11], "mm")
    print("31 January:", rain[len(rain) - 1], "mm")
