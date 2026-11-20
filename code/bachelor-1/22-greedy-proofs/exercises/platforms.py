"""platforms.py: the fewest platforms for a timetable of (arrival, departure) times,
a train occupying its platform from arrival to departure included."""


def platforms(trains):
    arrivals = sorted(a for a, _ in trains)
    departures = sorted(d for _, d in trains)
    busy = most = j = 0
    for a in arrivals:
        while j < len(departures) and departures[j] < a:  # left strictly before a
            busy -= 1
            j += 1
        busy += 1
        most = max(most, busy)
    return most
