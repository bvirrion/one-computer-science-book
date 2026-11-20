import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_factorial_power_sum():
    f = load("listings", "factorial")
    assert f.factorial(10) == 3628800 and f.power(3, 5) == 243
    assert f.sum_list(list(range(101))) == 5050


def test_hanoi_moves_are_legal_and_minimal():
    h = load("listings", "hanoi")
    for n in range(1, 11):
        moves = []
        h.hanoi(n, "A", "C", "B", moves)
        pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
        for disk, a, b in moves:
            assert pegs[a][-1] == disk
            assert not pegs[b] or pegs[b][-1] > disk
            pegs[b].append(pegs[a].pop())
        assert pegs["C"] == list(range(n, 0, -1)) and len(moves) == 2**n - 1


def test_koch_and_fib():
    k = load("listings", "koch")
    assert len(k.curve(3)) == 4**3 + 1
    ex = load("exercises", "recursion_ex")
    fibs = [0, 1]
    for _ in range(30):
        fibs.append(fibs[-1] + fibs[-2])
    for n in range(20):
        assert ex.fib_calls(n) == 2 * fibs[n + 1] - 1


def test_exercises():
    ex = load("exercises", "recursion_ex")
    assert ex.reverse("loop") == "pool" and ex.count_digits(2026) == 4
    assert ex.flatten([1, [2, [3, 4]], [], 5]) == [1, 2, 3, 4, 5]
    printed = []
    ex.show(3, printed)
    assert printed == [1, 2, 1, 3, 1, 2, 1]
    assert ex.is_palindrome("kayak") and not ex.is_palindrome("kayaks")
    assert sorted(map(tuple, ex.subsets([1, 2, 3]))) == sorted(
        [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)])
    assert all(ex.binary(n) == format(n, "b") for n in range(300))
    try:
        ex.factorial_checked(-1)
        raise AssertionError
    except ValueError:
        pass
