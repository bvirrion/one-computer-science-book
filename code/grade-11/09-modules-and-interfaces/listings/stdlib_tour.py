import random
import statistics
from collections import Counter
from datetime import date, timedelta

rng = random.Random(7)
print(rng.choice(["letter", "packet", "parcel"]))
print(statistics.median([3, 1, 4, 1, 5, 9]), statistics.median([3, 1, 4]))
print(Counter("abracadabra").most_common(3))
d = date.fromisoformat("2026-11-20")
print(d, d.weekday(), d + timedelta(days=100), date(2027, 1, 1) - d)
