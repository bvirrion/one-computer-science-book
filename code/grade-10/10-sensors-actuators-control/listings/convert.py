LOW, HIGH, LEVELS = -20.0, 60.0, 1024  # the sensor's range, on 10 bits


def to_celsius(raw):
    """Turn a reading 0..1023 into degrees: an offset and a scale."""
    return LOW + raw * (HIGH - LOW) / (LEVELS - 1)


if __name__ == "__main__":
    for raw in (0, 255, 511, 512, 1023):
        print(f"raw {raw:4} -> {to_celsius(raw):7.3f} degrees")
    print("one step is", round((HIGH - LOW) / (LEVELS - 1), 4), "degrees")
