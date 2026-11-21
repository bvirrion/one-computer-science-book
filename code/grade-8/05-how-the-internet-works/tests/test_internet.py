"""Grade 8, chapter 5: how the Internet works."""

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "listings"))

from packets import cut, rebuild  # noqa: E402


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "exercises" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def output(name):
    return (HERE / "outputs" / f"{name}.txt").read_text().splitlines()[1:]


def test_packets():
    message = "A fox in the garden at dusk!"
    packets = cut(message, 6, "a", "b")
    assert len(packets) == 5 and rebuild(packets[::-1]) == message
    assert output("lost_packet") == ["A fox ______ garden at dusk!"]
    assert output("ip_bytes")[-1].endswith("11000000101010000000000100010100")
    assert output("path")[0] == "A -> B -> C -> F in 3 steps"


def test_photo_trip():
    data = 1500 - 40
    packets = -(-3_000_000 // data)
    assert packets == 2055
    total = 3_000_000 + packets * 40
    propagation = 20_000 / (300_000 / 1.468)
    lines = output("photo_trip")
    assert lines[0] == f"{packets} packets, {packets * 40} bytes of headers, {total} bytes in all"
    assert lines[1].endswith(f"{propagation:.3f} s")
    assert f"{total * 8 / 10_000_000:.3f}" == "2.466"
    assert f"{total * 8 / 100_000_000:.3f}" == "0.247"
    assert abs(300_000 / 1.468 - 300_000 * 2 / 3) / 200_000 < 0.03


def test_exercises():
    pieces = load("cut10").cut("Meet me at the lighthouse at six.", 10)
    assert [p["data"] for p in pieces] == ["Meet me at", " the light", "house at s", "ix."]
    assert [p["number"] for p in pieces] == [1, 2, 3, 4] and all(p["of"] == 4 for p in pieces)
    assert [len(load("cut10").cut("x" * n, 10)) for n in (1, 10, 11, 20)] == [1, 1, 2, 2]
    assert all(p["of"] == len(load("cut10").cut("x" * n, 10)) for n in (1, 10, 11, 20)
               for p in load("cut10").cut("x" * n, 10))
    packets = cut("abcdefghijkl", 1, "a", "b")
    assert load("rebuild_bug").rebuild(packets) == "abklcdefghij"
    assert load("rebuild_fixed").rebuild(packets[::-1]) == "abcdefghijkl"
    assert load("valid_bug").is_valid("192.168.300.1")
    fixed = load("valid_fixed").is_valid
    assert not fixed("192.168.300.1") and fixed("192.168.1.20") and not fixed("1.2.3")
    same = load("same_network").same_network
    assert same("192.168.1.20", "192.168.1.31") and not same("192.168.1.20", "192.168.2.20")
    assert load("sending_time").sending_time(5_000_000, 20_000_000) == 2.0
    assert 2**32 == 4_294_967_296
    assert f"{6000 / (300_000 / 1.468) * 1000:.0f}" == "29"
    data = 1460
    n = -(-1_000_000 // data)
    assert (n, 1_000_000 + 40 * n) == (685, 1_027_400)
    twice = [packets[0], packets[2], packets[0], packets[3]]
    assert load("reassemble").reassemble(twice, 5) == ("acd", [1, 4])
