"""office_model.py: the ticket office's protocols, checked under every schedule."""
from interleavings import Model, report


def sell(s, me):
    if me["n"] > 0:
        s["sold"] = s["sold"] + (me["n"],)


def naive(customers):                             # check, then sell: three steps
    steps = []
    for _ in range(customers):
        steps += [("n = seats", None, lambda s, me: me.update(n=s["seats"])),
                  ("if n > 0: seats = n - 1", None,
                   lambda s, me: s.update(seats=me["n"] - 1) if me["n"] > 0 else None),
                  ("sell seat n", None, sell)]
    return steps


def locked(customers):                            # the same three steps under a lock
    steps = []
    for _ in range(customers):
        steps += [("lock", lambda s, me: s["lock"] == 0,
                   lambda s, me: s.update(lock=1))]
        steps += naive(1)
        steps += [("unlock", None, lambda s, me: s.update(lock=0))]
    return steps


def take(s, me):                                   # one indivisible step
    me["n"] = s["seats"]
    s["seats"] = max(s["seats"] - 1, 0)


def atomic(customers):
    steps = []
    for _ in range(customers):
        steps += [("n = take a seat", None, take), ("sell seat n", None, sell)]
    return steps


def office(protocol, seats, customers):
    def correct(s):                               # each seat sold once, none invented
        wanted = min(seats, 2 * customers)
        return sorted(s["sold"]) == list(range(1, wanted + 1))

    return Model({"seats": seats, "sold": (), "lock": 0},
                 {"A": protocol(customers), "B": protocol(customers)}, final=correct)


if __name__ == "__main__":
    report("check then sell, 1 seat, 1 customer per window", office(naive, 1, 1))
    report("locked, 1 seat, 1 customer per window", office(locked, 1, 1))
    report("locked, 6 seats, 4 customers per window", office(locked, 6, 4))
    report("atomic take, 6 seats, 4 customers per window", office(atomic, 6, 4))
