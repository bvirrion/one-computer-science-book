"""Conversions between degrees Celsius and degrees Fahrenheit (exercise 5)."""


def to_fahrenheit(c):
    """Return the temperature c, in degrees Celsius, in degrees Fahrenheit."""
    return c * 9 / 5 + 32


def to_celsius(f):
    """Return the temperature f, in degrees Fahrenheit, in degrees Celsius."""
    return (f - 32) * 5 / 9
