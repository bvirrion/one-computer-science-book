"""exo_switch.py: two switches in a line; their tables after six frames (exercise 5)."""
from switch_sim import Switch

s1, s2 = Switch([1, 2, 3]), Switch([1, 2, 3])
where = {"A": (s1, 1), "B": (s1, 2), "C": (s2, 2), "D": (s2, 3)}
link = {(s1, 3): (s2, 1), (s2, 1): (s1, 3)}   # port 3 of s1 is wired to port 1 of s2


def deliver(src, dst):
    todo = [where[src]]
    while todo:
        sw, port = todo.pop()
        for out in sw.receive(src, dst, port):
            if (sw, out) in link:
                todo.append(link[(sw, out)])


for src, dst in ["AC", "CA", "DB", "BD", "AB", "DC"]:
    deliver(src, dst)
for name, sw in (("s1", s1), ("s2", s2)):
    print(name, " ".join(f"{m}:{p}" for m, p in sorted(sw.table.items())))
