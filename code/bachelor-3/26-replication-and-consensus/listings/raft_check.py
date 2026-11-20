"""raft_check.py -- 1,000 seeded runs of five servers for 1,000 time units, with a
client command every 10 units and random crashes and restarts, and lost messages.
After each run the safety properties are checked."""

import random
import sys

from raft import cluster, leader


def one_run(seed, buggy_commit=False):
    net, servers = cluster(seed, buggy_commit=buggy_commit, loss=0.05)
    rng = random.Random(seed + 10**6)  # the schedule's own generator
    n = iter(range(10**6))

    def client():
        lead = leader(servers)
        if lead:
            lead.submit(f"c{next(n)}")

    for t in range(50, 1000, 10):
        net.at(t, client)
    for _ in range(rng.randint(2, 8)):
        t, s = rng.randint(50, 900), rng.choice(servers).name
        net.at(t, lambda s=s: net.procs[s].up and net.crash(s))
        net.at(t + rng.randint(20, 150), lambda s=s: net.procs[s].up or net.recover(s))
    net.run(until=1000)
    return check(net, servers)


def check(net, servers):
    """The names of the safety properties the run broke."""
    broken = set()
    terms = [t for t, _ in net.leaders]
    if len(terms) != len(set(terms)):
        broken.add("election safety")  # two leaders in one term
    if any(len(entries) > 1 for entries in net.committed.values()):
        broken.add(
            "state machine safety"
        )  # two different entries committed at one index
    for a in servers:
        for b in servers:
            for i in range(1, min(len(a.log), len(b.log)) + 1):
                if a.log[i - 1][0] == b.log[i - 1][0] and a.log[:i] != b.log[:i]:
                    broken.add("log matching")
    return broken, len(net.committed), len(net.leaders)


if __name__ == "__main__":
    buggy = "--buggy-commit" in sys.argv
    bad, committed, elections = {}, 0, 0
    for seed in range(1000):
        broken, c, e = one_run(seed, buggy)
        committed, elections = committed + c, elections + e
        for b in broken:
            bad[b] = bad.get(b, 0) + 1
    print(f"1000 runs: {committed} entries committed, {elections} leaders elected")
    for prop in ("election safety", "log matching", "state machine safety"):
        print(f"  {prop:<21} broken in {bad.get(prop, 0)} runs")
