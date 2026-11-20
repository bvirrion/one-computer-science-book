"""Three would-be deciders, each one defeated by its own contrarian program."""
import inspect
import sys

from contrarian import make_contrarian


class OutOfTime(Exception):
    pass


def run_for(f, x, budget):
    """Run f(x), but give up after budget lines of Python have been executed."""
    count = 0

    def tracer(frame, event, arg):
        nonlocal count
        if event == "line":
            count += 1
            if count > budget:
                raise OutOfTime
        return tracer

    sys.settrace(tracer)
    try:
        return f"stops, returning {f(x)!r}"
    except OutOfTime:
        return f"still running after {budget} lines"
    finally:
        sys.settrace(None)


def always_yes(program, data):
    return True


def always_no(program, data):
    return False


def no_endless_loop(program, data):
    """Looks at the source: a program without 'while True' is said to stop."""
    return "while True" not in inspect.getsource(program)


for decider in [always_yes, always_no, no_endless_loop]:
    c = make_contrarian(decider)
    claim = "stops" if decider(c, c) else "runs for ever"
    print(f"{decider.__name__:15} says c(c) {claim:13}; in fact c(c)",
          run_for(c, c, 100_000))
