import struct
import sys


def fields(x):
    """Return the sign, exponent and fraction bits of the 64-bit float x, as strings."""
    (n,) = struct.unpack(">Q", struct.pack(">d", x))
    bits = format(n, "064b")
    return bits[0], bits[1:12], bits[12:]


for x in (1.0, -2.5, 0.1):
    sign, exponent, fraction = fields(x)
    e = int(exponent, 2)
    print(f"{x:5}  sign {sign}  exponent {exponent} = {e} - 1023 = {e - 1023}")
    print(f"       fraction {fraction}")
print(float.hex(0.1))
print(sys.float_info.mant_dig, sys.float_info.max_exp, sys.float_info.max)
