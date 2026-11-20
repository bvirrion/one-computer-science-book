"""A simulated temperature sensor: 10-bit readings from -20 to +60 degrees, noisy."""

LOW, HIGH, LEVELS = -20.0, 60.0, 1024


def to_raw(celsius, rng, noise=0.3):
    """The 10-bit number the sensor reports for a true temperature."""
    measured = celsius + rng.gauss(0, noise)
    raw = round((measured - LOW) / (HIGH - LOW) * (LEVELS - 1))
    return min(max(raw, 0), LEVELS - 1)


def room(minutes, controller, rng, outside=8.0, start=17.0):
    """Simulate a heated room; return (temperature, heater) for each minute."""
    t, heater, trace = start, False, []
    for _ in range(minutes):
        heater = controller(to_raw(t, rng), heater)
        t += 0.02 * (outside - t) + (0.45 if heater else 0.0)
        trace.append((t, heater))
    return trace
