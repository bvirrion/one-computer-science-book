"""Exercise 5: a leader that commits an entry of an earlier term by counting its
copies. The scenario is scripted: elections happen only when a server is told to
time out, and cuts decide who hears whom."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "listings"))
import raft  # noqa: E402
from raft_check import check  # noqa: E402

ALL = {"S1", "S2", "S3", "S4", "S5"}


def scenario(buggy_commit):
    raft.ELECTION = (10**4, 2 * 10**4)  # no spontaneous elections
    try:
        net, servers = raft.cluster(seed=8, buggy_commit=buggy_commit)
        by = {s.name: s for s in servers}

        def timeout(name):
            return lambda: by[name].on_timer(("election", by[name].epoch))

        def cut(*groups):
            return lambda: net.partition(*groups)

        steps = [
            (1, timeout("S1")),  # S1 leader of term 1
            (10, lambda: by["S1"].submit("a")),  # committed everywhere
            (30, cut({"S1", "S2"}, ALL - {"S1", "S2"})),
            (31, lambda: by["S1"].submit("b")),  # reaches S2 only
            (40, lambda: net.crash("S1")),
            (41, cut({"S2"}, ALL - {"S2"})),
            (42, timeout("S5")),  # S5 leader of term 2, votes S3, S4, S5
            (50, cut({"S5"}, ALL - {"S5"})),
            (51, lambda: by["S5"].submit("c")),  # stays on S5
            (55, lambda: net.crash("S5")),
            (60, cut()),
            (61, lambda: net.recover("S1")),
            (62, timeout("S1")),  # term 2: S3 and S4 already voted for S5
            (66, timeout("S1")),  # S1 leader of term 3, sends b to S3 and S4
            (90, lambda: net.crash("S1")),
            (95, lambda: net.recover("S5")),
            (96, timeout("S5")),  # term 3: everyone voted for S1
            (100, timeout("S5")),  # term 4: S5's last log term, 2, beats their 1
            (115, lambda: by["S5"].submit("d")),
        ]
        for t, action in steps:
            net.at(t, action)
        net.run(until=200)
        committed = {i: sorted(e) for i, e in sorted(net.committed.items())}
        return check(net, servers)[0], committed, raft.show(net, servers)
    finally:
        raft.ELECTION = (30, 60)


if __name__ == "__main__":
    for buggy in (True, False):
        broken, committed, logs = scenario(buggy)
        print(f"buggy_commit={buggy}: broken {sorted(broken) or 'nothing'}")
        print(f"  committed: {committed}")
        print(logs)
