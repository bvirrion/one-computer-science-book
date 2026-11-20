"""Grade 8, chapter 2: dictionaries."""

import importlib.util
import io
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "listings"))

import ballots  # noqa: E402
import votes_dict  # noqa: E402
import votes_list  # noqa: E402


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "exercises" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def run(folder, name):
    r = subprocess.run([sys.executable, f"{name}.py"], cwd=HERE / folder, capture_output=True, text=True)
    return r.returncode, r.stdout.splitlines(), r.stderr


def lines(folder, name):
    code, out, _ = run(folder, name)
    assert code == 0
    return out


def test_listings():
    assert lines("listings", "contacts") == ["0612 345 678", "3 contacts", "False True"]
    code, _, err = run("listings", "key_error")
    assert code == 1 and "KeyError: 'Leo'" in err
    assert lines("listings", "change_walk")[0] == "{'apples': 9, 'plums': 20}"
    out = lines("listings", "count_letters")
    assert out[-1] == "e appears 3 times"
    out = lines("listings", "count_words")
    assert out[-1] == "fox {'the': 4, 'fox': 2, 'saw': 2, 'hen': 2, 'and': 1}"
    assert lines("listings", "books")[-1] == "2 of 3 books are from after 2000"


def test_votes():
    assert len(ballots.BALLOTS) == 40
    assert set(ballots.BALLOTS) == set(ballots.CANDIDATES)
    results, looked = votes_list.count_per_candidate(ballots.BALLOTS, ballots.CANDIDATES)
    counts, looked_once = votes_dict.count_once(ballots.BALLOTS)
    assert results == [counts[c] for c in ballots.CANDIDATES] == [9, 4, 11, 5, 8, 3]
    assert (looked, looked_once) == (240, 40)
    assert votes_dict.winner_and_margin(counts) == ("Chloe", 2)
    assert ballots.BALLOTS[:12].count("Chloe") == 4
    out = lines("listings", "votes_compare")
    assert "240 names looked at with lists, 40" in out[0]
    assert "8000 names looked at with lists, 400" in out[1]


def test_exercises():
    assert lines("exercises", "walk_items") == ["Sami", "Leo"]
    assert lines("exercises", "capitals") == ["Tokyo / not known"]
    code, _, err = run("exercises", "translate_bug")
    assert code == 1 and "KeyError: 'mouse'" in err
    assert lines("exercises", "translate_fixed") == ["le chat mange le mouse"]
    assert lines("exercises", "counts_bug") == ["{'a': 1, 'rose': 1, 'is': 1}"]
    assert load("most_frequent").most_frequent("b a b a b") == "b"
    assert load("invert").invert({"x": 1}) == {1: "x"}
    assert lines("exercises", "oldest") == ["The Lighthouse Cat"]
    assert load("group").group_by_first_letter(["ab", "b", "ac"]) == {"a": ["ab", "ac"], "b": ["b"]}
    assert len(set("a rose is a rose is a rose".split())) == 3
