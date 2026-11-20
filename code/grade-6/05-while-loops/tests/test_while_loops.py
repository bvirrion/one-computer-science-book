"""The listings and exercise solutions of grade 6, chapter 5."""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent


def out(folder, name, typed="", timeout=10):
    r = subprocess.run([sys.executable, name], cwd=HERE / folder, input=typed,
                       capture_output=True, text=True, timeout=timeout)
    assert r.returncode == 0
    return r.stdout.splitlines()


def collatz(n):
    steps, highest = 0, n
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
        highest = max(highest, n)
    return steps, highest


def test_listings():
    assert out("listings", "countdown.py") == ["5", "4", "3", "2", "1", "Lift-off!"]
    assert out("listings", "savings.py") == ["17 weeks: 51 coins"]
    assert out("listings", "sum_until_zero.py", "12\n7\n30\n0\n")[-1].endswith("Total: 49")
    assert out("listings", "average.py", "14\n9.5\n17\n12.5\n-1\n")[-1].endswith("4 marks, average 13.25")
    assert out("listings", "fixed_forever.py") == ["Saved 51 coins"]
    assert out("listings", "for_and_while.py") == [f"for: {n}" for n in (3, 2, 1)] + [f"while: {n}" for n in (3, 2, 1)]
    for n in [0, 7, 10, 99, 2026, 100000]:
        assert out("listings", "digits.py", f"{n}\n")[-1].endswith(f"Digits: {len(str(n))}")
    assert out("listings", "guess.py", "37\n50\n25\n37\n")[-1].endswith("Found in 3 guesses!")


def test_forever_never_reaches_50():
    seen = {3 * k for k in range(100)}
    assert 50 not in seen and 51 in seen


def test_collatz():
    assert collatz(6) == (8, 16) and collatz(7) == (16, 52)
    assert out("listings", "collatz.py", "27\n")[-1].endswith("steps: 111 highest: 9232")
    assert out("listings", "collatz_record.py") == ["start: 97 steps: 118"]
    assert max(range(1, 100), key=lambda s: collatz(s)[0]) == 97
    assert collatz(97) == (118, 9232)


def test_exercise_solutions():
    assert out("exercises", "by_two.py") == ["5", "3", "1"]
    assert out("exercises", "turns.py") == ["3", "9", "27", "81", "243"]
    assert out("exercises", "squares_total.py") == ["30"]
    assert out("exercises", "sum100.py") == ["5050"]
    assert out("exercises", "never_fixed.py") == [str(i) for i in range(10)]
    assert out("exercises", "total_bug.py") == ["45"]
    assert out("exercises", "total_fixed.py") == ["55"]
    assert out("exercises", "doubling.py") == ["1024 after 10 doublings"]
    assert out("exercises", "digit_sum.py", "2026\n")[-1].endswith("Sum of the digits: 10")
    assert out("exercises", "halving.py") == ["50", "25", "12", "6", "3", "1", "turns: 6"]
    assert out("exercises", "ask_yes.py", "no\nmaybe\nyes\n")[-1].endswith("Well done.")
    assert out("exercises", "guess_limit.py", "37\n50\n25\n37\n")[-1].endswith("Found in 3 guesses!")
    lose = "64\n" + "1\n" * 7
    assert out("exercises", "guess_limit.py", lose)[-1].endswith("The number was 64")
    # halving the interval: 7 guesses always suffice for 1..100
    assert 2 ** 7 > 100 > 2 ** 6
