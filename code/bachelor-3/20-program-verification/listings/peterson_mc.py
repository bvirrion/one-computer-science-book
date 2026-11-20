"""peterson_mc.py -- explicit-state model checking of Peterson's mutual exclusion for
two processes, and of a variant without turn that tests the other's flag before
raising its own. A state is (pc0, pc1, flag0, flag1, turn)."""

from collections import deque

from ctl import Kripke, show

IDLE, WANT, WAIT, CRIT = range(4)  # program counter values


def peterson(state, i):
    """The state after process i takes its next step, or None if it is blocked."""
    pc, flag, turn, j = list(state[:2]), list(state[2:4]), state[4], 1 - i
    match pc[i]:
        case 0:  # IDLE: flag[i] = 1
            flag[i], pc[i] = 1, WANT
        case 1:  # WANT: turn = j
            turn, pc[i] = j, WAIT
        case 2:  # WAIT: until flag[j] == 0 or turn == i
            if not (flag[j] == 0 or turn == i):
                return None
            pc[i] = CRIT
        case 3:  # CRIT: leave, flag[i] = 0
            flag[i], pc[i] = 0, IDLE
    return (*pc, *flag, turn)


def no_turn(state, i):
    pc, flag, j = list(state[:2]), list(state[2:4]), 1 - i
    match pc[i]:
        case 0:  # IDLE: wait until flag[j] == 0
            if flag[j]:
                return None
            pc[i] = WANT
        case 1:  # WANT: flag[i] = 1, then enter
            flag[i], pc[i] = 1, CRIT
        case 3:
            flag[i], pc[i] = 0, IDLE
    return (*pc, *flag, 0)


def explore(step, start=(IDLE, IDLE, 0, 0, 0)):
    """Breadth-first search of the reachable states, remembering how each was found."""
    parent, queue, succ = {start: None}, deque([start]), {}
    while queue:
        s = queue.popleft()
        succ[s] = set()
        for i in (0, 1):
            t = step(s, i)
            if t is not None:
                succ[s].add(t)
                if t not in parent:
                    parent[t] = (s, i)
                    queue.append(t)
    return succ, parent


def check(name, step):
    succ, parent = explore(step)
    labels = {s: {"true"} | {f"crit{i}" for i in (0, 1) if s[i] == CRIT} for s in succ}
    k = Kripke(succ, labels)
    start = (IDLE, IDLE, 0, 0, 0)
    for f in (("AG", ("not", ("and", "crit0", "crit1"))), ("AG", ("EF", "crit0"))):
        print(f"{name}: {len(succ)} reachable states; {show(f)}: {start in k.sat(f)}")
    bad = [s for s in succ if s[0] == s[1] == CRIT]
    if bad:  # breadth-first, so the first bad state found has a shortest trace
        s, trace = bad[0], [bad[0]]
        while parent[s]:
            s = parent[s][0]
            trace.append(s)
        print(
            f"  counterexample trace, {len(trace) - 1} steps (pc0, pc1, flag0, flag1):"
        )
        print("   ", " -> ".join(str(t[:4]) for t in reversed(trace)))


if __name__ == "__main__":
    check("Peterson", peterson)
    check("without turn", no_turn)
