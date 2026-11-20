"""Grade 8, chapter 1: binary and hexadecimal."""

import importlib.util
import io
import re
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CHAPTER = HERE.parent.parent.parent / "parts" / "grade-8" / "01-binary-and-hexadecimal.tex"


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def lines(folder, name):
    r = subprocess.run([sys.executable, f"{name}.py"], cwd=HERE / folder, capture_output=True, text=True)
    assert r.returncode == 0
    return r.stdout.splitlines()


def test_conversions():
    assert lines("listings", "to_decimal")[-1] == "101100 in binary is 44"
    assert lines("listings", "to_binary")[-1] == "binary: " + bin(44)[2:]
    to_binary = load("exercises", "to_binary_fn").to_binary
    for n in range(0, 600):
        assert to_binary(n) == bin(n)[2:]
    to_hex = load("listings", "to_hex").to_hex
    for n in range(256):
        assert to_hex(format(n, "08b")) == format(n, "02X")


def test_addition():
    add8 = load("listings", "add_binary").add_binary
    add_any = load("exercises", "add_any").add_binary
    for a in range(0, 256, 7):
        for b in range(0, 256, 11):
            assert int(add8(format(a, "08b"), format(b, "08b")), 2) == a + b
            assert int(add_any(bin(a)[2:], bin(b)[2:]), 2) == a + b
    assert 109 + 59 == 168 and 200 + 112 == 312 and 312 - 256 == 56


def test_colours():
    rgb = load("listings", "colours").rgb
    code = load("exercises", "to_code").colour_code
    tex = CHAPTER.read_text()
    for c in ["#FF8800", "#2E8B57", "#4169E1"]:
        assert code(*rgb(c)) == c
        # the swatch drawn in the chapter uses the same code as the listing
        assert re.search(r"\\definecolor\{[A-Za-z]+\}\{HTML\}\{" + c[1:] + r"\}", tex)


def test_patterns_and_grains():
    out = lines("listings", "count_patterns")
    for n in range(1, 11):
        assert out[n] == f"n = {n} : {2 ** n} patterns, largest number {2 ** n - 1}"
    out = lines("listings", "grains")
    assert out[-4] == "total: 18446744073709551615" and 18446744073709551615 == 2 ** 64 - 1
    assert out[-1] == "hexadecimal: " + "F" * 16


def test_exercises():
    assert lines("exercises", "downwards_bug") == ["011"]
    assert lines("exercises", "is_binary")[1] == "102 is not a binary number"
    assert lines("exercises", "convert") == ["2C 11111111", "377 200221"]
    convert = load("exercises", "convert").convert
    for n in range(0, 300, 13):
        for b in range(2, 17):
            assert convert(convert(str(n), 10, b), b, 10) == str(n)
    assert 2 ** 12 == 4096 and 2 ** 16 - 1 == 65535 == 0xFFFF
