"""raft_partition.py -- the leader and one follower are cut off from the other three.
Both sides receive client commands; only the side with a majority commits them."""

from raft import cluster, show

net, servers = cluster(seed=26)
by = {s.name: s for s in servers}
pictures = []


def submit(name, cmd):
    ok = by[name].submit(cmd)
    net.notes.append(f"t={net.now:>3} client sends {cmd} to {name}: accepted={ok}")


def note(text, action):
    return lambda: (action(), net.notes.append(f"t={net.now:>3} {text}"))


net.at(60, lambda: submit("S5", "x=1"))
net.at(
    70,
    note(
        "cut: {S1, S5} | {S2, S3, S4}",
        lambda: net.partition({"S5", "S1"}, {"S2", "S3", "S4"}),
    ),
)
net.at(80, lambda: submit("S5", "y=2"))
net.at(90, lambda: submit("S5", "z=3"))
net.at(160, lambda: submit("S2", "y=9"))
net.at(199, lambda: pictures.append(show(net, servers)))
net.at(200, note("the cut is healed", lambda: net.partition()))
net.run(until=260)
pictures.append(show(net, servers))
print("\n".join(net.notes))
print("\n".join(pictures))
