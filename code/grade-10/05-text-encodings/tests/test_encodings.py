import importlib.util
import io
import random
from contextlib import redirect_stdout
from pathlib import Path

import pytest

HERE = Path(__file__).parent.parent
rng = random.Random(2026)


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        try:
            spec.loader.exec_module(module)
        except UnicodeDecodeError:
            pass  # the staged error of decode_error.py
    return module


def random_code_points(n):
    points = []
    while len(points) < n:
        cp = rng.choice([rng.randint(0, 0x7F), rng.randint(0x80, 0x7FF),
                         rng.randint(0x800, 0xFFFF), rng.randint(0x10000, 0x10FFFF)])
        if not 0xD800 <= cp <= 0xDFFF:
            points.append(cp)
    return points


def test_utf8_encode_by_hand():
    enc = load("listings", "utf8_by_hand").utf8_encode
    for cp in random_code_points(2000):
        assert enc(cp) == chr(cp).encode("utf-8")


def test_utf8_decode_and_length():
    dec = load("exercises", "utf8_decode").utf8_decode
    length = load("exercises", "utf8_length").utf8_length
    points = random_code_points(500)
    text = "".join(map(chr, points))
    assert dec(text.encode("utf-8")) == points
    for cp in points:
        assert length(cp) == len(chr(cp).encode("utf-8"))


def test_is_ascii():
    is_ascii = load("exercises", "is_ascii").is_ascii
    for s in ["", "abc ~", "Café", "\x7f", "\x80"]:
        assert is_ascii(s) == s.isascii()


def test_fix_mojibake():
    fix = load("exercises", "fix_mojibake").fix_mojibake
    board = load("exercises", "notice_board")
    once = board.garble(board.MESSAGE, 1)
    assert fix(once) == board.MESSAGE
    assert fix(fix(board.garble(board.MESSAGE, 2))) == board.MESSAGE
    assert fix("plain text") == "plain text" and fix("Café") == "Café"


def test_cut_bytes():
    mod = load("exercises", "cut_bytes")
    with pytest.raises(UnicodeDecodeError):
        mod.cut_buggy("Café", 4)
    for _ in range(300):
        text = "".join(map(chr, random_code_points(rng.randint(0, 8))))
        n = rng.randint(0, 20)
        out = mod.cut(text, n)
        assert text.startswith(out) and len(out.encode()) <= n
        if len(out) < len(text):
            assert len(text[: len(out) + 1].encode()) > n


def test_notice_board_numbers():
    board = load("exercises", "notice_board")
    assert board.name_sizes() == {"utf-8": 301, "utf-16-le": 600, "latin-1": 300}
    assert board.ungarble(board.garble(board.MESSAGE, 2), 2) == board.MESSAGE
    assert "Ã©" in board.garble("é", 1)


def test_ascii_table_rows():
    out = (HERE / "outputs" / "ascii_table.txt").read_text().splitlines()
    assert out[3].split()[1:] == [chr(c) for c in range(0x30, 0x40)]
