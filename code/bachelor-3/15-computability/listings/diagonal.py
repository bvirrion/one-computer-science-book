"""diagonal.py -- any claimed halting decider halts(f, x) is wrong about one program:
the paradox built from it. Four candidate deciders, each refuted on its own paradox."""
import inspect
import sys

BUDGET = 100_000  # Python lines; a run still going after this is reported as running


def run_with_budget(f, x):
    """'halted', or 'is still running' after BUDGET lines of f(x)."""
    count = 0

    def tracer(frame, event, arg):
        nonlocal count
        count += event == "line"
        if count > BUDGET:
            raise TimeoutError
        return tracer
    sys.settrace(tracer)
    try:
        f(x)
        return "halted"
    except TimeoutError:
        return "is still running"
    finally:
        sys.settrace(None)


def make_paradox(halts):
    def paradox(f):
        if halts(f, f):  # the decider says f(f) halts: then loop for ever
            while True:
                pass
        return "done"  # the decider says it loops: then halt at once
    return paradox


CANDIDATES = {
    "always yes": lambda f, x: True,
    "always no": lambda f, x: False,
    "no 'while' in the source": lambda f, x: "while" not in inspect.getsource(f),
    "short source": lambda f, x: len(inspect.getsource(f)) < 400,
}

if __name__ == "__main__":
    for name, halts in CANDIDATES.items():
        p = make_paradox(halts)
        said = "halts" if halts(p, p) else "loops"
        print(f"{name:<26} says paradox(paradox) {said:<5}; "
              f"it {run_with_budget(p, p)}")
    print(f"(budget: {BUDGET:,} Python lines)")
