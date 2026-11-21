import math
import wave
from pathlib import Path

RATE = 8000        # samples per second
FREQUENCY = 440    # hertz
samples = bytes(round(127.5 + 127 * math.sin(2 * math.pi * FREQUENCY * k / RATE))
                for k in range(RATE))

with wave.open("tone.wav", "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(1)  # one byte per sample: 8 bits
    w.setframerate(RATE)
    w.writeframes(samples)

print("first samples:", list(samples[:10]))
size = Path("tone.wav").stat().st_size
print("file size:", size, "bytes for", len(samples), "samples")
# capture: scratch
