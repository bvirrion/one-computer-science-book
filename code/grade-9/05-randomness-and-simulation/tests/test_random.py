"""Grade 9, chapter 5: randomness and simulation."""

import importlib.util
import io
import math
import random
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "listings"))


def run(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    out = io.StringIO()
    with redirect_stdout(out):
        spec.loader.exec_module(module)
    return module, out.getvalue()


def test_tiny_generator_cycles():
    module, out = run("listings", "tiny_generator")
    assert "after 16 numbers" in out
    for start in range(16):                     # every start: the full cycle
        x, seen = start, set()
        while x not in seen:
            seen.add(x)
            x = module.next_number(x)
        assert len(seen) == 16


def test_seed_repeats():
    _, out = run("listings", "seed_demo")
    lines = out.splitlines()
    assert lines[0] == lines[1] != lines[2]


def test_exact_values():
    _, out = run("listings", "birthday_exact")
    assert out.splitlines()[-1] == "smallest class above one half: 23 (0.5073)"
    birthday, _ = run("listings", "birthday")
    random.seed(1)
    assert abs(birthday.frequency(23, 4000) - 0.507) < 0.03
    assert birthday.shared(366) is True
    _, out = run("listings", "sum_seven")
    assert "exact: 6 ways out of 36, 0.1667" in out


def test_walk_and_figures():
    walk, _ = run("listings", "random_walk")
    random.seed(11)
    path = walk.walk(100)
    assert len(path) == 101 and all(abs(a - b) == 1 for a, b in zip(path, path[1:]))
    subprocess.run([sys.executable, str(HERE / "figures" / "random_figures.py")],
                   check=True)
    dat = (HERE / "figures" / "out" / "walk.dat").read_text().split()
    assert dat[-1] == str(path[-1])
    freq = (HERE / "figures" / "out" / "frequency.dat").read_text().splitlines()
    assert len(freq) == 14 and freq[-1].startswith("100000 ")


def test_exercises():
    assert run("exercises", "longest_heads")[1].strip().endswith(": 7")
    counts = eval(run("exercises", "die_bug")[1])
    assert len(counts) == 7 and all(abs(c - 10_000) < 400 for c in counts)
    assert run("exercises", "seed_loop_bug")[1].strip() == "[1, 1, 1, 1, 1, 1, 1, 1]"
    fixed = run("exercises", "seed_loop_fixed")[1].strip()
    assert fixed == "[1, 3, 5, 5, 6, 1, 2, 5]"
    assert "exact: 3/51 = 0.0588" in run("exercises", "pair_chance")[1]
    assert "back home along the grid: 6" in run("exercises", "grid_walk")[1]
    out = run("exercises", "walk_return")[1]
    assert f"exact: {math.comb(20, 10)} paths of 1048576, 0.1762" in out
