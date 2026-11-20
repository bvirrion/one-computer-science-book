"""Two processes, two locks: every run, and the ones where both wait for ever."""


def explore(p, q):
    """Return the runs that end with both processes blocked."""
    stuck = []

    def go(i, j, owner, trace):
        moves = []
        for who, prog, k in [("P", p, i), ("Q", q, j)]:
            if k < len(prog):
                action, lock = prog[k]
                if action == "take" and owner.get(lock) not in (None, who):
                    continue                     # held by the other one: wait
                moves.append((who, action, lock))
        if not moves:
            if i < len(p) or j < len(q):         # nobody can move, and work is left
                wants = {"P": p[i][1], "Q": q[j][1]}
                stuck.append((trace, {who: owner[wants[who]] for who in wants}))
            return
        for who, action, lock in moves:
            o = dict(owner)
            o[lock] = who if action == "take" else None
            step = f"{who} {action}s {lock}"
            go(i + (who == "P"), j + (who == "Q"), o, trace + [step])

    go(0, 0, {}, [])
    return stuck


def cycle(waits_for, start):
    """Follow 'who waits for whom' from start; return the cycle met, or None."""
    path, who = [], start
    while who is not None and who not in path:
        path.append(who)
        who = waits_for.get(who)
    return path[path.index(who):] + [who] if who is not None else None


def run_pair(p_order, q_order):
    p = [("take", x) for x in p_order] + [("free", x) for x in p_order]
    q = [("take", x) for x in q_order] + [("free", x) for x in q_order]
    return explore(p, q)


stuck = run_pair("AB", "BA")
print("P takes A then B, Q takes B then A:", len(stuck), "runs end in a deadlock")
trace, waits_for = stuck[0]
print("  for instance:", ", ".join(trace))
print("  wait-for graph:", waits_for, "cycle:", " -> ".join(cycle(waits_for, "P")))
print("both take A then B:", len(run_pair("AB", "AB")), "runs end in a deadlock")
