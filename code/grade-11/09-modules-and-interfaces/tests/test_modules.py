import importlib
import io
import os
import random
import subprocess
import sys
from contextlib import redirect_stdout
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent.parent
for folder in ("listings", "exercises", "exercises/side_effect"):
    sys.path.insert(0, str(HERE / folder))


def quiet_import(name):
    with redirect_stdout(io.StringIO()) as out:
        module = importlib.import_module(name)
    return module, out.getvalue()


def test_geometry_and_rewrite():
    geometry, _ = quiet_import("geometry")
    rewrite, _ = quiet_import("geometry_zip")
    rng = random.Random(9)
    for _ in range(100):
        pts = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(rng.randint(2, 8))]
        assert abs(geometry.perimeter(pts) - rewrite.perimeter(pts)) < 1e-9
    assert geometry.perimeter([(0, 0), (3, 0), (3, 3), (0, 3)]) == 12


def test_three_implementations_agree():
    impls = [quiet_import(n)[0] for n in ("dateset_list", "dateset_set", "dateset_sorted")]
    rng = random.Random(4)
    sets = [ds.empty() for ds in impls]
    for _ in range(300):
        d = date(2026, 1, 1) + timedelta(days=rng.randrange(60))
        answers = {ds.contains(s, d) for ds, s in zip(impls, sets)}
        assert len(answers) == 1
        for ds, s in zip(impls, sets):
            ds.add(s, d)
        assert len({ds.size(s) for ds, s in zip(impls, sets)}) == 1


def test_temperature_and_counts():
    t, _ = quiet_import("temperature")
    assert t.to_fahrenheit(100) == 212 and t.to_celsius(-40) == -40
    ex, _ = quiet_import("modules_ex")
    assert ex.ex4() == (5.0, [("a", 3), ("n", 2)])
    assert ex.ex10() == (1024, 1024.0)
    assert ex.word_count("A b a. B a!", 2) == [("a", 3), ("b", 2)]


def test_chosen_at_import():
    for env, kind in (("list", list), ("set", set)):
        os.environ["DATESET"] = env
        sys.modules.pop("dates_chosen", None)
        chosen, _ = quiet_import("dates_chosen")
        assert type(chosen.empty()) is kind
    del os.environ["DATESET"]


def test_staged_faults():
    run = subprocess.run([sys.executable, "stops.py"], cwd=HERE / "exercises/circular",
                         capture_output=True, text=True)
    assert "partially initialized module 'lines'" in run.stderr
    primes, printed = quiet_import("primes")
    fixed, printed_fixed = quiet_import("primes_fixed")
    assert printed.startswith("computing") and printed_fixed == ""
    assert all(primes.is_prime(n) == fixed.is_prime(n) for n in range(2000))
