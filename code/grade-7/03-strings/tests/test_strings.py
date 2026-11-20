"""Grade 7, chapter 3: strings."""

import importlib.util
import io
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def out(folder, name):
    r = subprocess.run([sys.executable, f"{name}.py"], cwd=HERE / folder, capture_output=True, text=True)
    return r.returncode, r.stdout.splitlines(), r.stderr


def lines(folder, name):
    code, o, _ = out(folder, name)
    assert code == 0
    return o


def test_listings():
    assert lines("listings", "string_basics") == ["6", "P y n", "n o", "Python!!!"]
    code, _, err = out("listings", "immutable")
    assert code == 1 and "does not support item assignment" in err
    assert lines("listings", "rebuild") == ["Jami"]
    assert lines("listings", "slices") == ["key", "board", "key board", "board", "draobyek"]
    text = "Once upon a time, a fox lived in a quiet wood."
    assert lines("listings", "vowels")[0] == f"vowels: {sum(c in 'aeiouAEIOU' for c in text)}"
    assert lines("listings", "words")[1:3] == ["8 words", "3 times the"]
    assert lines("listings", "codes") == ["65 97 48 32", "HI", "G", "'", "G G", "233 122"]
    assert lines("listings", "palindrome") == ["level True", "Kayak True", "Never odd or even True", "Python False"]


def test_passage_and_figure():
    o = lines("listings", "passage_stats")
    rows = (HERE / "figures" / "out" / "letters.dat").read_text().split("\n")[1:-1]
    counts = {r.split()[0]: int(r.split()[1]) for r in rows}
    for line in o[3:]:
        letter, n = line.split()
        assert counts[letter] == int(n)
    assert int(o[1].split()[1]) == sum(counts.values())


def test_palindrome_dates():
    m = load("listings", "dates")
    assert m.two(7) == "07" and m.two(12) == "12"
    assert m.date_string(2, 2, 2020) == "02022020"
    assert m.days_in_month(2, 2092) == 29 and m.days_in_month(2, 2100) == 28
    found = []
    for y in range(2001, 2100):
        for mo in range(1, 13):
            for d in range(1, m.days_in_month(mo, y) + 1):
                s = f"{d:02}{mo:02}{y}"
                if s == s[::-1]:
                    found.append(s)
    assert len(found) == 29 and found[0] == "10022001" and found[-1] == "29022092"
    o = lines("listings", "all_dates")
    assert o[0] == "29 palindrome dates" and o[1] == "first: 10-02-2001  last: 29-02-2092"
    assert sum(len(line.split()) for line in o[2:]) == 29


def test_exercises():
    assert lines("exercises", "spaces") == ["6 6"]
    assert lines("exercises", "palindrome_bug") == ["False"]
    assert lines("exercises", "palindrome_fixed") == ["True"]
    assert lines("exercises", "initials") == ["A.L.", "G.B.H."]
    assert lines("exercises", "star_vowels") == ["*nc* *p*n * t*m*"]
    assert lines("exercises", "longest_word") == ["quick"]
    assert lines("exercises", "mirror") == [
        "bid bid True", "bud bud True", "pod boq False", "pq pq True", "box xod False"
    ]
    s = "keyboard!!"
    assert s[::-1][::-1] == s and all(s[:k] + s[k:] == s for k in range(len(s) + 1))
    assert len([s[i:i + 3] for i in range(len(s) - 2)]) == 8
