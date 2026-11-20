import random

from convert import to_celsius
from sensor import to_raw

rng = random.Random(10)
values = [to_celsius(to_raw(20.0, rng)) for _ in range(30)]  # the true value is 20.0


def moving_average(xs, width):
    """The mean of each window of `width` consecutive values."""
    return [sum(xs[i - width + 1:i + 1]) / width for i in range(width - 1, len(xs))]


smooth = moving_average(values, 5)
print("raw:     ", [round(v, 1) for v in values[:8]])
print("smoothed:", [round(v, 1) for v in smooth[:8]])
print("spread raw", round(max(values) - min(values), 2),
      " smoothed", round(max(smooth) - min(smooth), 2))
