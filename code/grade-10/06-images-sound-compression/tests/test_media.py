import importlib.util
import io
import math
import random
import wave
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
rng = random.Random(2026)


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_rle_round_trip_and_fixed_encoder():
    rle = load("listings", "rle")
    bugs = load("exercises", "rle_bugs")
    for _ in range(300):
        s = "".join(rng.choice("WB") for _ in range(rng.randint(0, 30)))
        assert rle.rle_decode(rle.rle_encode(s)) == s
        assert bugs.rle_encode(s) == rle.rle_encode(s)
    assert bugs.rle_encode_buggy("WWB") == [(2, "W")]


def test_demosaic_known_pixels():
    d = load("listings", "demosaic")
    assert d.rgb_at(1, 1) == (185, 118, 60)
    assert d.colour_of(0, 0) == "R" and d.colour_of(1, 1) == "B"


def test_quantise_error_at_most_half_step():
    q = load("listings", "quantise").quantise
    for levels in (2, 4, 8, 16, 256):
        step = 255 / (levels - 1)
        assert all(abs(g - q(g, levels)) <= step / 2 + 0.5 for g in range(256))


def test_samples_plot_dat():
    fig = load("figures", "samples_plot")
    text = fig.OUT.read_text().splitlines()
    assert text[0] == "ms value level" and len(text) == 22
    for line in text[1:]:
        _, value, level = map(float, line.split())
        assert abs(value - level) <= 1 / 7 + 1e-5


def test_histogram():
    h = load("exercises", "pgm_histogram").histogram("P2\n3 2\n4\n0 1 1\n4 4 4\n")
    assert h == [1, 2, 0, 0, 3]


def test_wav_duration(tmp_path):
    dur = load("exercises", "wav_duration").wav_duration
    path = tmp_path / "t.wav"
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(8000)
        w.writeframes(bytes(4 * 12000))
    assert dur(path) == 1.5


def test_bitmap_ratio():
    mod = load("exercises", "rle_bitmap")
    rows = ["WWWWBBBB", "WWWWWWWW"]
    assert mod.bitmap_ratio(rows) == (16, 3, 16 / 6)


def test_aliasing():
    a = load("exercises", "aliasing")
    assert abs(a.measured_frequency(a.sampled(440, 8000), 8000) - 440) <= 1
    assert abs(a.measured_frequency(a.sampled(7000, 8000), 8000) - 1000) <= 1


def test_minute_of_music():
    m = load("exercises", "minute_of_music")
    assert 60 * m.bytes_per_second() == 10_584_000
    song = m.music(1)
    assert len(song) == 176_400
    assert len(song) / len(__import__("zlib").compress(song, 9)) < 1.2
    assert math.isclose(10_584_000 / 2**20, 10.09, abs_tol=0.005)
