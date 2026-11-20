"""Exercise 15: a tone sampled too slowly seems to have another frequency."""
import math


def sampled(frequency, rate, seconds=1):
    return [math.sin(2 * math.pi * frequency * k / rate) for k in range(rate * seconds)]


def measured_frequency(samples, rate):
    """Count the sign changes from negative to non-negative per second."""
    ups = sum(1 for a, b in zip(samples, samples[1:]) if a < 0 <= b)
    return ups * rate / len(samples)
