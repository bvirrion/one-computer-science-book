"""Grade 9, chapter 7: the maze game project."""

import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent.parent
LISTINGS = HERE / "listings"
sys.path.insert(0, str(LISTINGS))

import maze_v5  # noqa: E402
from maze_v5 import can_move, check_level, move, parse_level, read_text, won  # noqa: E402
from try_all_moves import all_sequences, wins  # noqa: E402

SMALL = "5\n#####\n#Sg=#\n###T#\n#####\n"


@pytest.fixture(autouse=True)
def in_listings(monkeypatch):
    monkeypatch.chdir(LISTINGS)


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    out = io.StringIO()
    with redirect_stdout(out):
        spec.loader.exec_module(module)
    return module, out.getvalue()


def test_check_and_parse():
    assert check_level(read_text("level1.txt")) == ""
    assert check_level(read_text("bad_level.txt")) == "a level needs exactly one S and one T"
    assert check_level("3\n###\n#S#T#\n") == "every row must have the same length"
    state = parse_level(read_text("level1.txt"))
    assert [state["row"], state["col"], state["gems_left"], state["moves_left"]] == [1, 1, 2, 20]
    assert state["grid"][1][1] == "."


def test_rules_on_a_small_grid():
    state = parse_level(SMALL)
    assert not can_move(state, "w") and can_move(state, "d")
    move(state, "d")                               # the only gem: the gate opens
    assert state["gems_left"] == 0 and state["grid"][1][3] == "."
    assert can_move(state, "d")
    move(state, "d")
    move(state, "s")
    assert won(state) and state["moves_left"] == 2


def test_gate_stays_closed_until_the_last_gem():
    state = parse_level(read_text("level1.txt"))
    for key in "ssss":
        move(state, key)
    assert state["gems_left"] == 1 and "=" in state["grid"][2]


def test_play_win_and_loss(monkeypatch):
    for name, expected in [["maze_v5", True], ["lost_game", False]]:
        keys = iter((LISTINGS / f"{name}.stdin").read_text().split())
        monkeypatch.setattr("builtins.input", lambda prompt, keys=keys: next(keys))
        with redirect_stdout(io.StringIO()):
            assert maze_v5.play("level1.txt") is expected


def test_all_moves():
    assert len(all_sequences(3)) == 64 and len(set(all_sequences(3))) == 64
    tiny = read_text("tiny.txt")
    assert [s for s in all_sequences(6) if wins(tiny, s)] == ["ddssaa"]
    assert not any(wins(read_text("level2.txt"), s) for s in all_sequences(6))


def test_exercises():
    wait, _ = load("exercises", "wait_move")
    state = parse_level(read_text("level1.txt"))
    move(state, "x")
    assert [state["row"], state["col"], state["moves_left"]] == [1, 1, 19]
    del maze_v5.MOVES["x"]
    assert load("exercises", "wrap_bug")[1].strip() == "True True False"
    assert load("exercises", "wrap_fixed")[1].strip() == "False False False"
    replay, _ = load("exercises", "replay")
    assert replay.replay(read_text("level1.txt"), "wssssddddwsddwwww") == 16
    assert replay.replay(read_text("level1.txt"), "ssss") == -1
    gate, _ = load("exercises", "gate_bug")
    state = parse_level(read_text("level1.txt"))
    for key in "ss":
        gate.move(state, key)
    assert state["gems_left"] == 1 and "=" not in state["grid"][2]   # opened too soon
    tele, _ = load("exercises", "teleport")
    state = parse_level("9\n#######\n#So..o#\n#####T#\n#######\n")
    tele.move_teleport(state, "d")
    assert [state["row"], state["col"]] == [1, 5]
    checker, _ = load("exercises", "checker")
    assert checker.winnable(read_text("tiny.txt"), 6)
    assert not checker.winnable(read_text("level2.txt"), 6)
    fog, _ = load("exercises", "fog")
    with redirect_stdout(io.StringIO()) as out:
        fog.draw_fog(parse_level(read_text("level1.txt")), 1)
    assert out.getvalue().splitlines()[0] == "###??????"
    shortest, _ = load("exercises", "shortest")
    assert shortest.shortest(read_text("tiny.txt"), 7) == "ddssaa"
