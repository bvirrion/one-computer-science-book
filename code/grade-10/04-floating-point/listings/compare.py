import math

a = 0.1 + 0.2
print(a == 0.3, math.isclose(a, 0.3))
print(math.isclose(1e-12, 0.0), math.isclose(1e-12, 0.0, abs_tol=1e-9))

big = 1e308 * 10
print(big, -big, big - big)
nan = big - big
print(nan == nan, math.isnan(nan), max(nan, 1.0), max(1.0, nan))
print(0.0 == -0.0, math.copysign(1.0, -0.0))
