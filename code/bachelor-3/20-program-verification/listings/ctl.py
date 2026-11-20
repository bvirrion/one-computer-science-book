"""ctl.py -- a model checker for computation tree logic over an explicit Kripke
structure. EX, EU and EG are computed directly; EU as a least fixed point, EG as a
greatest one. The other operators are abbreviations."""


class Kripke:
    def __init__(self, succ, labels):
        self.succ, self.labels = succ, labels  # state -> successors, state -> props
        self.states = set(succ)

    def pre(self, target):
        """EX: the states with at least one successor in target."""
        return {s for s in self.states if self.succ[s] & target}

    def sat(self, f):
        match f:
            case str(p):
                return {s for s in self.states if p in self.labels[s]}
            case ("not", g):
                return self.states - self.sat(g)
            case ("and", g, h):
                return self.sat(g) & self.sat(h)
            case ("or", g, h):
                return self.sat(g) | self.sat(h)
            case ("EX", g):
                return self.pre(self.sat(g))
            case ("EU", g, h):  # least fixed point of Z = h or (g and EX Z)
                keep, z = self.sat(g), self.sat(h)
                while (bigger := z | (keep & self.pre(z))) != z:
                    z = bigger
                return z
            case ("EG", g):  # greatest fixed point of Z = g and EX Z
                z = self.sat(g)
                while (smaller := z & self.pre(z)) != z:
                    z = smaller
                return z
            case ("EF", g):
                return self.sat(("EU", "true", g))
            case ("AX", g):
                return self.sat(("not", ("EX", ("not", g))))
            case ("AG", g):
                return self.sat(("not", ("EF", ("not", g))))
            case ("AF", g):
                return self.sat(("not", ("EG", ("not", g))))
        raise ValueError(f)


def show(f):
    """Formulas as text: ("AG", ("EF", "done")) is AG EF done."""
    if isinstance(f, str):
        return f
    if f[0] in ("and", "or"):
        return f"({show(f[1])} {f[0]} {show(f[2])})"
    return f"{f[0]} {show(f[1])}"


if __name__ == "__main__":
    k = Kripke(
        succ={0: {1, 2}, 1: {1}, 2: {3}, 3: {0, 3}},
        labels={
            0: {"true", "start"},
            1: {"true", "busy"},
            2: {"true", "busy"},
            3: {"true", "done"},
        },
    )
    for f in (
        "done",
        ("EX", "done"),
        ("EF", "done"),
        ("AF", "done"),
        ("EG", "busy"),
        ("AG", ("EF", "done")),
        ("EF", ("AG", "busy")),
    ):
        print(f"{show(f):<16} holds in states {sorted(k.sat(f))}")
    # every path ends in p forever (LTL: F G p), yet AF AG p fails in state 0
    k2 = Kripke(
        succ={0: {0, 1}, 1: {2}, 2: {2}},
        labels={0: {"true", "p"}, 1: {"true"}, 2: {"true", "p"}},
    )
    print(
        "second structure: AF AG p holds in states", sorted(k2.sat(("AF", ("AG", "p"))))
    )
