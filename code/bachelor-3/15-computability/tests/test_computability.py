"""Tests for chapter 15: the machines, the simulators, the reduction, the busy beaver."""
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for d in ("listings", "exercises"):
    sys.path.insert(0, os.path.join(HERE, "..", d))

import busy_beaver  # noqa: E402
import diagonal  # noqa: E402
import ex5_increment  # noqa: E402
import ex6_anbn  # noqa: E402
import ex12_primrec as ex12  # noqa: E402
import multitape  # noqa: E402
import primrec  # noqa: E402
import reductions  # noqa: E402
import utm  # noqa: E402
from machines import ADD, INCREMENT, PALINDROME  # noqa: E402
from tm import accepts, run  # noqa: E402


def words(alphabet, n):
    for k in range(n + 1):
        yield from ("".join(w) for w in itertools.product(alphabet, repeat=k))


def test_increment_and_add():
    for n in range(256):
        assert run(INCREMENT, bin(n)[2:])[2] == bin(n + 1)[2:]
    for a, b in itertools.product(range(1, 6), repeat=2):
        assert run(ADD, "1" * a + "+" + "1" * b)[2] == "1" * (a + b)


def test_palindromes_one_and_two_tapes():
    for w in words("ab", 8):
        assert accepts(PALINDROME, w) == (w == w[::-1])
        state, steps = multitape.run2(multitape.PAL2, w, start="copy")
        assert (state == "accept") == (w == w[::-1])
        if w == w[::-1]:  # exercise 9
            assert steps == 3 * len(w) + 3
            assert run(PALINDROME, w)[3] == (len(w) + 1) * (len(w) + 2) // 2


def test_exercise_4_predictions():
    assert run(INCREMENT, "1111")[2:] == ("10000", 10)
    assert run(ADD, "1+1")[2] == "11"
    assert run(PALINDROME, "aa")[3] == 6


def test_primitive_recursion_and_ackermann():
    for x, y in itertools.product(range(6), repeat=2):
        assert primrec.add(x, y) == x + y and primrec.mul(x, y) == x * y
        assert primrec.power(x, y) == y ** x
    for n in range(6):
        assert primrec.ackermann(1, n) == n + 2
        assert primrec.ackermann(2, n) == 2 * n + 3
        assert primrec.ackermann(3, n) == 2 ** (n + 3) - 3
    # the text: A(4, 0) = A(3, 1), A(4, 1) = A(3, A(4, 0)) = 2^16 - 3
    assert primrec.ackermann(4, 0) == primrec.ackermann(3, 1) == 13
    sys.set_int_max_str_digits(0)
    assert 2 ** (13 + 3) - 3 == 65_533 and len(str(2 ** 65536 - 3)) == 19_729


def test_universal_program_agrees():
    for delta, alphabet in ((INCREMENT, "01"), (PALINDROME, "ab"), (ADD, "1+")):
        code, symbols = utm.encode(delta)
        assert set(code) <= set("01#")
        for w in words(alphabet, 6):
            direct, via = run(delta, w), utm.universal(code, symbols, w)
            assert (direct[0], direct[2], direct[3]) == (via[0], via[2], via[3])


def test_every_candidate_decider_is_wrong():
    for halts in diagonal.CANDIDATES.values():
        p = diagonal.make_paradox(halts)
        said = halts(p, p)
        assert (diagonal.run_with_budget(p, p) == "halted") != said


def test_reduction_preserves_halting():
    loop_on_0 = {("q0", "0"): ("q0", "0", "S")}  # halts exactly when w starts with 1
    for delta in (INCREMENT, reductions.RUN_RIGHT, loop_on_0):
        for w in words("01", 4):
            halts = run(delta, w, max_steps=1000)[0]
            m = reductions.reduce(delta, w)
            for x in ("", "1", "0110"):
                assert accepts(m, x, start="erase", max_steps=5000) == halts


def test_busy_beaver_small():
    assert busy_beaver.busy_beaver(1)[:4] == (64, 32, 1, 1)
    total, halting, s, sigma, champion = busy_beaver.busy_beaver(2)
    assert (total, halting, s, sigma) == (20_736, 9_784, 6, 4)
    assert busy_beaver.run(champion) == (6, 4)
    actions = list(itertools.product((0, 1), (-1, 1), [0, 1, "H"]))
    for m in itertools.product(actions, repeat=4):  # nothing halts after step 6
        r = busy_beaver.run(m, cap=1000)
        assert r is None or r[0] <= 6


def test_exercise_5_increment_fix():
    assert run(ex5_increment.BUGGY, "111")[2] == "000"
    for n in range(256):
        assert run(ex5_increment.FIXED, bin(n)[2:])[2] == bin(n + 1)[2:]


def test_exercise_6_anbn():
    for w in words("ab", 8):
        n = len(w) // 2
        assert accepts(ex6_anbn.ANBN, w) == (w == "a" * n + "b" * n)


def test_exercise_12_primitive_recursive():
    assert ex12.pred(0) == 0 and ex12.pred(5) == 4
    for x, y in itertools.product(range(13), repeat=2):
        assert ex12.monus(x, y) == max(x - y, 0)
        if y > 0:
            assert ex12.div(x, y) == x // y and ex12.rem(x, y) == x % y
