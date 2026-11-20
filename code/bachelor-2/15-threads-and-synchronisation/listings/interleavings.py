"""interleavings.py: run small thread models under every possible schedule."""
import textwrap
from collections import Counter
from math import comb


class Model:
    """Threads are lists of steps (label, guard, action) over shared and local dicts.

    guard(s, me) says whether the step may run now (None: always); action(s, me)
    changes the dicts and may return the index of the next step (None: the next
    one). A thread whose next step is labelled "critical section" is inside it.
    """

    def __init__(self, shared, threads, final=None, outcome=None):
        self.shared, self.threads = shared, threads
        self.final, self.outcome = final, outcome


def freeze(d):
    return tuple(sorted(d.items()))


def explore(model):
    """Count the schedules, the bad ones and the stuck ones; keep one bad schedule."""
    names = list(model.threads)
    progs = [model.threads[n] for n in names]
    memo = {}

    def go(pcs, sh, los):
        key = (pcs, sh, los)
        if key in memo:
            return memo[key]
        s = dict(sh)
        inside = sum(pc < len(p) and p[pc][0] == "critical section"
                     for pc, p in zip(pcs, progs))
        total, bad, stuck, example, outs = 0, 0, 0, None, Counter()
        for i, (pc, prog) in enumerate(zip(pcs, progs)):
            if pc == len(prog):
                continue
            label, guard, action = prog[pc]
            if guard and not guard(s, dict(los[i])):
                continue
            s2, l2 = dict(s), dict(los[i])
            jump = action(s2, l2) if action else None
            new_pcs = pcs[:i] + (pc + 1 if jump is None else jump,) + pcs[i + 1:]
            new_los = los[:i] + (freeze(l2),) + los[i + 1:]
            t, b, k, ex, o = go(new_pcs, freeze(s2), new_los)
            total, bad, stuck, outs = total + t, bad + b, stuck + k, outs + o
            if b and example is None:
                example = [f"{names[i]}: {label}"] + ex
        if total == 0:                               # nobody can move: an end
            done = all(pc == len(p) for pc, p in zip(pcs, progs))
            total, stuck = 1, 0 if done else 1
            bad = int(done and model.final is not None and not model.final(s))
            example = [] if bad else None
            if model.outcome:
                outs = Counter([model.outcome(s)])
        if inside > 1:                               # mutual exclusion violated here
            bad, example = total, []
        memo[key] = (total, bad, stuck, example, outs)
        return memo[key]

    start = tuple(0 for _ in progs)
    los = tuple(freeze({}) for _ in progs)
    return go(start, freeze(model.shared), los)


def report(title, model):
    total, bad, stuck, example, outs = explore(model)
    line = f"{title}: {total} schedules, {bad} bad"
    if stuck:
        line += f", {stuck} stuck"
    if outs:
        line += "; outcomes " + ", ".join(f"{v} ({n})" for v, n in sorted(outs.items()))
    print(line)
    if example:
        text = "e.g. " + " | ".join(example)
        print(textwrap.fill(text, 88, initial_indent="   ", subsequent_indent=" " * 8))


def counter_thread(increments):
    steps = []
    for _ in range(increments):
        steps.append(("r = x", None, lambda s, me: me.update(r=s["x"])))
        steps.append(("x = r + 1", None, lambda s, me: s.update(x=me["r"] + 1)))
    return steps


def counter(increments=1):
    return Model({"x": 0}, {"A": counter_thread(increments),
                            "B": counter_thread(increments)},
                 final=lambda s: s["x"] == 2 * increments,
                 outcome=lambda s: s["x"])


def flag_lock_thread():
    return [
        ("wait until flag == 0", lambda s, me: s["flag"] == 0, None),
        ("flag = 1", None, lambda s, me: s.update(flag=1)),
        ("critical section", None, None),
        ("flag = 0", None, lambda s, me: s.update(flag=0)),
    ]


def peterson_thread(i):
    j = 1 - i
    return [
        (f"flag{i} = 1", None, lambda s, me: s.update({f"flag{i}": 1})),
        (f"turn = {j}", None, lambda s, me: s.update(turn=j)),
        (f"wait until flag{j} == 0 or turn == {i}",
         lambda s, me: s[f"flag{j}"] == 0 or s["turn"] == i, None),
        ("critical section", None, None),
        (f"flag{i} = 0", None, lambda s, me: s.update({f"flag{i}": 0})),
    ]


def peterson():
    return Model({"flag0": 0, "flag1": 0, "turn": 0},
                 {"A": peterson_thread(0), "B": peterson_thread(1)})


def straight(m, n):
    """Two threads of m and n steps that never wait."""
    return Model({}, {"A": [(f"a{k}", None, None) for k in range(m)],
                      "B": [(f"b{k}", None, None) for k in range(n)]})


if __name__ == "__main__":
    report("two threads, 3 and 4 steps", straight(3, 4))
    print(f"   binomial(7, 3) = {comb(7, 3)}")
    report("counter, one increment each", counter(1))
    report("naive flag lock", Model({"flag": 0}, {"A": flag_lock_thread(),
                                                   "B": flag_lock_thread()}))
    report("Peterson", peterson())
