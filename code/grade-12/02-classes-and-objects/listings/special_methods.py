class Duration:
    """A length of time, in whole minutes."""

    def __init__(self, minutes):
        self.minutes = minutes

    def __repr__(self):                   # for programmers: how to rebuild it
        return f"Duration({self.minutes})"

    def __str__(self):                    # for people
        return f"{self.minutes // 60} h {self.minutes % 60:02}"

    def __eq__(self, other):
        return self.minutes == other.minutes

    def __lt__(self, other):
        return self.minutes < other.minutes

    def __add__(self, other):
        return Duration(self.minutes + other.minutes)


class Playlist:
    def __init__(self, name, durations):
        self.name, self.durations = name, list(durations)

    def __len__(self):
        return len(self.durations)


songs = [Duration(4), Duration(71), Duration(12)]
print(songs, "|", songs[1])
print(sorted(songs), max(songs), Duration(4) == Duration(4))
print(sum(songs, Duration(0)))
print(len(Playlist("morning", songs)))
