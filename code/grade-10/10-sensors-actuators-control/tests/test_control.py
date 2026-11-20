import importlib.util
import io
import random
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).parent.parent
sys.path.insert(0, str(HERE / "listings"))
sys.path.insert(0, str(HERE / "exercises"))


def load(folder, name):
    spec = importlib.util.spec_from_file_location(name, HERE / folder / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def test_conversion_round_trip():
    conv = load("listings", "convert")
    sensor = load("listings", "sensor")
    rng = random.Random(1)
    for t in (-10.0, 0.0, 20.0, 37.5):
        assert abs(conv.to_celsius(sensor.to_raw(t, rng, noise=0)) - t) <= 0.04
    assert sensor.to_raw(100.0, rng) == 1023 and sensor.to_raw(-50.0, rng) == 0
    c = load("exercises", "controllers")
    assert c.to_celsius(512) == conv.to_celsius(512)


def test_hysteresis_switches_less():
    th = load("listings", "thermostat")
    sensor = load("listings", "sensor")
    count = []
    for ctl in (th.plain, th.hysteresis):
        trace = sensor.room(360, ctl, random.Random(4))
        count.append(sum(1 for a, b in zip(trace, trace[1:]) if a[1] != b[1]))
    assert count == [214, 77]


def test_controllers():
    c = load("exercises", "controllers")
    table = {("red", "tick"): "green"}
    assert c.next_state(table, "red", "button") == "red"
    try:
        c.next_state_buggy(table, "red", "button")
        raise AssertionError("expected a KeyError")
    except KeyError:
        pass
    trace = [19.6, 19.4, 19.6, 19.3, 19.7, 17.8, 19.8, 21.2, 19.4, 19.6]
    assert c.switches(trace, c.thermostat) == 2
    assert c.switches(trace, lambda t, h: t < 19.5) == 8
    s = (0, "down")
    for e in ["car at entry"] * 4 + ["car at exit"]:
        s = c.barrier(s, e)
    assert s == (2, "down")


def test_lift_safety_and_reachable():
    lift = load("listings", "lift")
    lc = load("exercises", "lift_check")
    c = load("exercises", "controllers")
    states = lc.reachable()
    assert len(states) == 12 and all(lift.safe(s) for s in states)
    assert c.check_safe(states, lc.EVENTS, lift.step, lift.safe) == []
    opened = lc.reachable(start=(0, "open", "stop", None), step=c.lift_step_buggy)
    assert any(not lift.safe(s) for s in opened)
    assert lc.serve([2, 0, 1, 2, 1]) == [3, 4, 3, 3, 3]


def test_thermostat_dat():
    fig = load("figures", "thermostat_plot")
    fig.main()
    lines = fig.OUT.read_text().splitlines()
    assert len(lines) == 122 and lines[0].startswith("minute")
