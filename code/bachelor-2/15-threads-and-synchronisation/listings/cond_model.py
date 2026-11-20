"""cond_model.py: a condition wait under if and under while (exercise 6).

One producer puts 2 items; two consumers take 1 each. wait() releases the lock
and sleeps until a signal moves the thread to the "woken" set; it then needs the
lock again before it goes on.
"""
from interleavings import Model, report


def lock():
    return ("lock", lambda s, me: s["owner"] == 0,
            lambda s, me: s.update(owner=1))


def unlock():
    return ("unlock", None, lambda s, me: s.update(owner=0))


def consumer(name, loop):
    def check(s, me):                             # step 1: test the condition
        return 4 if s["count"] > 0 else None      # jump to take, or go on to wait

    def wait(s, me):                              # step 2: release and sleep
        s.update(owner=0, waiting=s["waiting"] + (name,))

    def take(s, me):
        s.update(count=s["count"] - 1, bad=s["bad"] or s["count"] == 0)

    woken = ("wake, lock again",
             lambda s, me: name in s["woken"] and s["owner"] == 0,
             lambda s, me: s.update(owner=1, woken=tuple(w for w in s["woken"]
                                                         if w != name))
             or (1 if loop else 4))
    return [lock(), ("count > 0?", None, check), ("wait", None, wait), woken,
            ("take an item", None, take), unlock()]


def signal(s, me):                                # wake one waiting thread, if any
    if s["waiting"]:
        s.update(woken=s["woken"] + s["waiting"][:1], waiting=s["waiting"][1:])


def producer():
    one = [lock(), ("count += 1", None, lambda s, me: s.update(count=s["count"] + 1)),
           ("signal", None, signal), unlock()]
    return one + one


def model(loop):
    shared = {"owner": 0, "count": 0, "waiting": (), "woken": (), "bad": False}
    return Model(shared, {"P": producer(), "C1": consumer("C1", loop),
                          "C2": consumer("C2", loop)},
                 final=lambda s: not s["bad"])


if __name__ == "__main__":
    report("if around the wait", model(False))
    report("while around the wait", model(True))
