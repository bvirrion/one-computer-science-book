"""Every typing drill uses only the keys its source comment declares, on the real layout,
and every timed passage prints its true character count."""

import re
from pathlib import Path

import pytest
import xkblayout

REPO = Path(__file__).resolve().parents[4]
TEX = REPO / "parts" / "typing" / "01-typing-drills.tex"
STY = REPO / "styles" / "onecs.sty"

pytestmark = pytest.mark.skipif(not xkblayout.ROOT.is_dir(), reason="no xkb symbol files")

DRILL = re.compile(r"^\\omdrill\{([^\\{}]*)\}% drill: (\w+) keys=(\S+)( shift)?$")
PASSAGE = re.compile(r"^\\ompassage\{(\d+)\}\{([^\\{}]*)\}% drill: (\w+) keys=(\S+)( shift)?$")


def expand(keys, layout):
    if keys == "all":
        return set(layout)
    out = set()
    for part in keys.split(","):
        a, _, b = part.partition("-")
        if not b:
            out.add(a)
            continue
        assert a[:2] == b[:2], part
        out.update(f"{a[:2]}{i:02d}" for i in range(int(a[2:]), int(b[2:]) + 1))
    return out


def typable(layout, keys, shift):
    chars = {" "}
    for k in keys:
        syms = layout[k]
        for level, sym in enumerate(syms[:2]):
            if level == 1 and not shift:
                break
            c = xkblayout.char(sym)
            if c:
                chars.add(c)
    return chars


def lines():
    out = []
    for n, line in enumerate(TEX.read_text().splitlines(), 1):
        if line.startswith("\\omdrill"):
            m = DRILL.match(line)
            assert m, f"line {n}: a drill without a well-formed '% drill:' comment"
            out.append((n, m.group(1), m.group(2), m.group(3), bool(m.group(4)), None))
        elif line.startswith("\\ompassage"):
            m = PASSAGE.match(line)
            assert m, f"line {n}: a passage without a well-formed '% drill:' comment"
            out.append((n, m.group(2), m.group(3), m.group(4), bool(m.group(5)), int(m.group(1))))
    return out


@pytest.fixture(scope="module")
def layouts():
    return {name: xkblayout.load(name) for name in ("us", "fr", "de")}


def test_drill_lines_use_only_their_keys(layouts):
    found = lines()
    assert len(found) > 90
    for n, text, lay, keys, shift, _ in found:
        ok = typable(layouts[lay], expand(keys, layouts[lay]), shift)
        bad = sorted(set(text) - ok)
        assert not bad, f"line {n} ({lay}): {bad} not typable with keys={keys}{' shift' if shift else ''}"


def test_passage_counts(layouts):
    passages = [x for x in lines() if x[5] is not None]
    assert len(passages) == 9
    for n, text, _lay, _keys, _shift, count in passages:
        assert len(text) == count, f"line {n}: printed {count}, the passage has {len(text)} characters"


def test_each_layout_has_every_kind_of_line():
    for lay in ("us", "fr", "de"):
        mine = [x for x in lines() if x[2] == lay]
        assert any(x[3].startswith("AC") and "AD" not in x[3] for x in mine), lay   # home row
        assert any("AB" in x[3] for x in mine), lay                                 # bottom row
        assert any(x[4] and x[3] != "all" for x in mine), lay                       # capitals
        assert any("AE" in x[3] for x in mine), lay                                 # digits
        assert sum(x[5] is not None for x in mine) == 3, lay                        # passages


def test_keyboard_letter_legends_match_layouts(layouts):
    """The drawn keyboards (\\omkeyboard in styles/onecs.sty) print the capital that the
    layout's level 2 types, on every letter key."""
    legends = re.findall(r"^\\omkb@one\{(\w+)\}\{(\w+)\}\{(.)\}$", STY.read_text(), re.M)
    assert len(legends) > 70
    for lay, key, cap in legends:
        assert xkblayout.char(layouts[lay][key][1]) == cap, (lay, key, cap)
