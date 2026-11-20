"""raft_election.py -- five servers start as followers; the first timeout wins."""

from raft import cluster

net, servers = cluster(seed=26)
net.run(until=120)
print("\n".join(net.notes))
print("terms:", " ".join(f"{s.name}:{s.term}" for s in servers))
