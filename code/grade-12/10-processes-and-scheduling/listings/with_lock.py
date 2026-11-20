"""The same two processes, with a lock around the three steps: every possible run."""


def program(name):
    return [(name, a) for a in ["acquire", "load", "add", "store", "release"]]


def explore(p, q):
    """Final counter of every complete run; a step waits while the lock is taken."""
    finals = []

    def go(i, j, holder, counter, reg):
        if i == len(p) and j == len(q):
            finals.append(counter)
            return
        for who, prog, k in [("P", p, i), ("Q", q, j)]:
            if k == len(prog):
                continue
            _, action = prog[k]
            if action == "acquire" and holder is not None:
                continue                         # blocked: the lock is taken
            h, c, r = holder, counter, dict(reg)
            if action == "acquire":
                h = who
            elif action == "release":
                h = None
            elif action == "load":
                r[who] = c
            elif action == "add":
                r[who] += 1
            else:
                c = r[who]
            go(i + (who == "P"), j + (who == "Q"), h, c, r)

    go(0, 0, None, 0, {})
    return finals


finals = explore(program("P"), program("Q"))
print(len(finals), "possible runs; final counter:", sorted(set(finals)))
