"""bakery_model.py: Lamport's bakery for three threads, every schedule (exercise 11)."""
from interleavings import Model, report

N = 3


def bakery_thread(i, rounds=1):
    steps = []
    for _ in range(rounds):
        steps.append((f"choosing{i} = 1", None,
                      lambda s, me: s.update({f"choosing{i}": 1}) or me.update(mx=0)))
        for j in range(N):                        # read the tickets one at a time
            steps.append((f"read number{j}", None,
                          lambda s, me, j=j: me.update(mx=max(me["mx"], s[f"n{j}"]))))
        steps.append((f"number{i} = max + 1", None,
                      lambda s, me: s.update({f"n{i}": me["mx"] + 1})))
        steps.append((f"choosing{i} = 0", None,
                      lambda s, me: s.update({f"choosing{i}": 0})))
        for j in range(N):
            if j == i:
                continue
            steps.append((f"wait until choosing{j} == 0",
                          lambda s, me, j=j: s[f"choosing{j}"] == 0, None))
            steps.append((f"wait until thread {j} is served after {i}",
                          lambda s, me, j=j: s[f"n{j}"] == 0
                          or (s[f"n{j}"], j) > (s[f"n{i}"], i), None))
        steps.append(("critical section", None, None))
        steps.append((f"number{i} = 0", None, lambda s, me: s.update({f"n{i}": 0})))
    return steps


def bakery(rounds=1):
    shared = {f"{v}{i}": 0 for v in ("choosing", "n") for i in range(N)}
    return Model(shared, {chr(65 + i): bakery_thread(i, rounds) for i in range(N)})


def no_choosing(rounds=1):                        # the same without the choosing flags
    model = bakery(rounds)
    for name, steps in model.threads.items():
        model.threads[name] = [st for st in steps if "choosing" not in st[0]]
        model.threads[name][0:0] = [("start", None, lambda s, me: me.update(mx=0))]
    return model


if __name__ == "__main__":
    report("bakery, 3 threads, one pass each", bakery())
    report("bakery, 3 threads, two passes each", bakery(2))
    report("bakery without choosing, 3 threads", no_choosing())
