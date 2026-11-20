import math

for x in (1.0, 2.0, 1000.0, 2.0**52, 2.0**53):
    up = math.nextafter(x, math.inf)
    print(f"{x:>18}  next float up {up:>20}  gap {math.ulp(x)}")
print(2.0**53 + 1 == 2.0**53)
print(1.0 + 2.0**-53 == 1.0, 1.0 + 2.0**-52 == 1.0)
