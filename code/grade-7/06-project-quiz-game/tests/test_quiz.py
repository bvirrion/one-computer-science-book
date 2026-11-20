"""Grade 7, project: the quiz game, played with scripted answers.

`monkeypatch` (a pytest helper) replaces Python's `input` by a function that returns the next
scripted answer, so the tests can play a whole game without a keyboard.
"""

import importlib.util
import io
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "listings"))

import questions  # noqa: E402
import quiz_v2  # noqa: E402
import quiz_v3  # noqa: E402
import quiz_v4  # noqa: E402
import quiz_v5  # noqa: E402


def script(monkeypatch, answers):
    typed = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(typed))


def quietly(function, *args):
    with redirect_stdout(io.StringIO()) as out:
        value = function(*args)
    return value, out.getvalue().splitlines()


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / "exercises" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def output(name):
    r = subprocess.run([sys.executable, f"{name}.py"], cwd=HERE / "listings",
                       input=(HERE / "listings" / f"{name}.stdin").read_text(),
                       capture_output=True, text=True)
    assert r.returncode == 0
    return r.stdout


def test_lists():
    assert len(questions.EASY_QUESTIONS) == len(questions.EASY_ANSWERS) == 10
    assert len(questions.HARD_QUESTIONS) == len(questions.HARD_ANSWERS) == 10
    namespace = {}
    with redirect_stdout(io.StringIO()):
        exec((HERE / "listings" / "quiz_v1.py").read_text(), namespace)
    assert namespace["questions"] == questions.EASY_QUESTIONS
    assert namespace["answers"] == questions.EASY_ANSWERS
    assert all(a == quiz_v2.normalise(a) for a in questions.EASY_ANSWERS + questions.HARD_ANSWERS)


def test_ask_and_play(monkeypatch):
    assert quiz_v2.normalise("  Paris ") == "paris"
    script(monkeypatch, ["  PARIS "])
    assert quietly(quiz_v2.ask, "Capital?", "paris")[0] == 1
    script(monkeypatch, ["Paris", "eight", "56", "jupiter", " Honey ", "60", "hot", "6", "green", "63"])
    assert quietly(quiz_v3.play, questions.EASY_QUESTIONS, questions.EASY_ANSWERS)[0] == 8
    for answers, points in [(["x", "paris"], 0.5), (["paris"], 1), (["x", "y"], 0)]:
        script(monkeypatch, answers)
        assert quietly(quiz_v4.ask, "Capital?", "paris")[0] == points
    assert "Your score: 3 out of 10" in output("quiz_v3_poor")
    assert "Your score: 8.5 out of 10" in output("quiz_v4")
    assert output("quiz_v5").splitlines()[-1] == "RESULT level=easy score=8.0/10"
    assert quiz_v5.result_line("hard", 8.5, 10) == "RESULT level=hard score=8.5/10"


def test_worst_game_lines():
    # on a terminal each typed answer ends its line: count the lines of the captured session
    shown = (HERE / "outputs" / "quiz_v5_worst.txt").read_text().splitlines()[1:]
    assert len(shown) == 1 + 10 * 3 + 1


def test_exercises(monkeypatch):
    skip = load("skip")
    script(monkeypatch, ["skip"])
    assert quietly(skip.ask, "Capital?", "paris") == (0, ["Skipped."])
    bug = load("ask_bug")
    script(monkeypatch, ["paris", "paris"])
    assert quietly(bug.ask, "Capital?", "paris")[0] == 1.5
    quit_ = load("quit")
    script(monkeypatch, ["paris", "8", "quit"])
    assert quietly(quit_.play, questions.EASY_QUESTIONS, questions.EASY_ANSWERS)[0] == 2
    assert load("streak").longest_streak([1, 0.5, 1, 1, 1, 0, 1, 1, 0.5, 1]) == 3
    many = load("many_answers")
    for typed in ["8", " Eight "]:
        script(monkeypatch, [typed])
        assert quietly(many.ask, many.QUESTIONS[0], many.ANSWERS[0])[0] == 1
    reachable = {a + 0.5 * b for a in range(11) for b in range(11 - a)}
    assert reachable == {k / 2 for k in range(21)}
