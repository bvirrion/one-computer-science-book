"""Exercise 14: the small root of x**2 + b*x + c, naive and stable."""
import math


def small_root_naive(b, c):
    """Smaller root in size of x**2 + b*x + c (b > 0, b*b > 4*c > 0), usual formula."""
    return (-b + math.sqrt(b * b - 4 * c)) / 2


def small_root_stable(b, c):
    """The same root as c / (large root): no subtraction of nearly equal numbers."""
    large = (-b - math.sqrt(b * b - 4 * c)) / 2
    return c / large
