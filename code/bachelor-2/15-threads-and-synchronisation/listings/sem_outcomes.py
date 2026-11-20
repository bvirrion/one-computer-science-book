"""sem_outcomes.py: every output of exo_sem.c, by the explorer (exercise 5)."""
from interleavings import Model, explore


def out(c):
    return (f"print {c}", None, lambda s, me: s.update(out=s["out"] + c))


def post(sem):
    return (f"post({sem})", None, lambda s, me: s.update({sem: s[sem] + 1}))


def wait(sem):                                    # may run only when the value is > 0
    return (f"wait({sem})", lambda s, me: s[sem] > 0,
            lambda s, me: s.update({sem: s[sem] - 1}))


def model():
    one = [out("A"), post("s"), out("C"), wait("t"), out("E")]
    two = [out("B"), wait("s"), out("D"), post("t")]
    return Model({"out": "", "s": 0, "t": 0}, {"one": one, "two": two},
                 outcome=lambda s: s["out"])


if __name__ == "__main__":
    total, bad, stuck, _, outs = explore(model())
    print(f"{total} schedules, {stuck} stuck, {len(outs)} different outputs:")
    for text, n in sorted(outs.items()):
        print(f"   {text}  ({n} schedules)")
