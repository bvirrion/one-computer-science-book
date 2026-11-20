import random
import zlib

samples = {
    "repeated text": b"the cat sat on the mat. " * 400,
    "zeros": bytes(10_000),
    "random bytes": random.Random(1).randbytes(10_000),
}
for name, data in samples.items():
    packed = zlib.compress(data, 9)
    same = zlib.decompress(packed) == data
    print(f"{name:14} {len(data):6} -> {len(packed):6} bytes"
          f"  ratio {len(data) / len(packed):7.1f}  same back: {same}")
