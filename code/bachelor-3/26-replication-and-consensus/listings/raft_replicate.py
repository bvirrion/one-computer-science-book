"""raft_replicate.py -- the leader replicates commands while S2 is down; then the
leader, cut off from the others, appends one more command, crashes, and a new leader
takes over. Logs are printed as term:command before and after the change."""

from raft import cluster, leader, show

net, servers = cluster(seed=26)
cmds = iter(["x=1", "y=2", "x=3", "z=4", "y=5", "x=6", "z=7", "y=8"])
pictures = []


def client():
    lead = leader(servers)
    if lead is None or not lead.submit(next(cmds)):
        net.at(net.now + 5, client)  # no leader yet: try again later


def logs():
    pictures.append(show(net, servers))


def event(t, text, action):
    net.at(t, lambda: (net.notes.append(f"t={t:>3} {text}"), action()))


for t in (60, 70, 80, 90, 100, 110, 115, 180):
    net.at(t, client)
others = {"S1", "S2", "S3", "S4"}
event(75, "S2 crashes", lambda: net.crash("S2"))
net.at(105, lambda: net.recover("S2"))
event(108, "S5 is cut off from the others", lambda: net.partition({"S5"}, others))
event(112, "S5 crashes; the cut is healed", lambda: (net.crash("S5"), net.partition()))
net.at(113, logs)
net.at(220, lambda: net.recover("S5"))
net.run(until=300)
logs()
print("\n".join(net.notes))
print("\n".join(pictures))
