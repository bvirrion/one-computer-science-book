"""Grade 9, chapter 6: a first look at cryptography."""

import importlib.util
import io
import math
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent.parent
LISTINGS = HERE / "listings"
sys.path.insert(0, str(LISTINGS))

from guess_shift import guess_key  # noqa: E402
from keyword_cipher import keyword_encrypt  # noqa: E402
from shift import encrypt  # noqa: E402
from substitution import ALPHABET, random_key, substitute  # noqa: E402


@pytest.fixture(autouse=True)
def in_listings(monkeypatch):
    monkeypatch.chdir(LISTINGS)


def run(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "exercises" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    out = io.StringIO()
    with redirect_stdout(out):
        spec.loader.exec_module(module)
    return module, out.getvalue().strip()


def test_ciphers_undo():
    text = "the keeper lit the lamp, at nine!"
    for key in range(26):
        assert encrypt(encrypt(text, key), -key) == text
    assert encrypt(text, 26) == text
    key = random_key(2026)
    assert sorted(key) == list(ALPHABET)
    assert substitute(substitute(text, ALPHABET, key), key, ALPHABET) == text
    assert encrypt("code", 3) == "frgh" and encrypt("qeb", -23) == "the"
    decrypt, _ = run("keyword_decrypt")
    assert decrypt.keyword_decrypt(keyword_encrypt(text, "lamp"), "lamp") == text


def test_counts_and_guesses():
    assert math.factorial(26) == 403_291_461_126_605_635_584_000_000
    out = (HERE / "outputs" / "guess_shift.txt").read_text()
    assert "whole message right: True" in out
    assert guess_key(encrypt("eeee and more", 7)) == 7
    subprocess.run([sys.executable, str(HERE / "figures" / "letter_counts.py")],
                   check=True)
    dat = (HERE / "figures" / "out" / "letters.dat").read_text().split("\n")
    assert dat[5] == "e 213 21" and dat[8] == "h 129 213"


def test_exercises():
    assert run("shift_case")[1] == "Phhw Ph dw Qrrq, eb wkh Crr!"
    assert run("shift_bug")[1] == "d { }"
    assert run("decrypt_bug")[1] == "coo iye kd dro rkblyeb"
    assert run("best_guess")[1] == "the keeper lit the lamp at the end of the day"
    assert run("all_keys_time")[1] == "12,788,288,341 years"
    assert run("short_counts")[1].splitlines()[2].startswith("1000 letters: ['e 150'")
    out = run("repeats")[1].splitlines()
    divides = [int(line.split()[3]) for line in out[1:]]
    assert divides.index(max(divides[1:])) == 2        # among 3 to 8, length 4 wins
