import wave
from pathlib import Path

pixels = bytes([255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 255])  # 2 x 2, RGB
Path("tiny.ppm").write_bytes(b"P6\n2 2\n255\n" + pixels)
data = Path("tiny.ppm").read_bytes()
magic, width, height, maxval = data.split(maxsplit=4)[:4]
print("PPM:", magic, int(width), int(height), int(maxval), len(data), "bytes")

with wave.open("click.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(44100)
    w.writeframes(bytes(4 * 441))
with wave.open("click.wav", "rb") as r:
    print("WAV:", r.getnchannels(), "channels,", 8 * r.getsampwidth(), "bits,",
          r.getframerate(), "Hz,", r.getnframes(), "frames")
print(Path("click.wav").read_bytes()[:16])
# capture: scratch
