"""Problem: a minute of disc-quality stereo; lossless compression barely helps."""
import math
import random
import zlib

RATE, BYTES_PER_SAMPLE, CHANNELS = 44100, 2, 2


def bytes_per_second():
    return RATE * BYTES_PER_SAMPLE * CHANNELS


def music(seconds, seed=2026):
    """Synthetic music: three tones and a little noise, 16-bit stereo, little-endian."""
    rng = random.Random(seed)
    out = bytearray()
    for k in range(RATE * seconds):
        t = k / RATE
        x = (0.4 * math.sin(2 * math.pi * 220 * t)
             + 0.3 * math.sin(2 * math.pi * 277.2 * t)
             + 0.2 * math.sin(2 * math.pi * 329.6 * t)
             + 0.05 * rng.uniform(-1, 1))
        v = round(x * 32767)
        out += v.to_bytes(2, "little", signed=True) * CHANNELS
    return bytes(out)


def runs(data):
    count = 1
    for a, b in zip(data, data[1:]):
        if a != b:
            count += 1
    return count


if __name__ == "__main__":
    print("bytes per second:", bytes_per_second())
    minute = 60 * bytes_per_second()
    print("one minute:", minute, "bytes =", round(minute / 2**20, 2), "MiB")
    song = music(1)
    silence = bytes(len(song))
    for name, data in (("music", song), ("silence", silence)):
        packed = zlib.compress(data, 9)
        ratio = len(data) / len(packed)
        print(f"{name:8} {len(data)} bytes, {runs(data)} runs,"
              f" zlib {len(packed)} bytes, ratio {ratio:.2f}")
