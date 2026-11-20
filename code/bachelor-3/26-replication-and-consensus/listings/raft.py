"""raft.py -- Raft as a state machine on netsim (chapter 25). Each server keeps its
current term, its vote and its log on 'disk' (they survive a crash); everything else
is lost when it crashes. Log index i is self.log[i - 1], an entry (term, command)."""

import sys
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[2] / "25-distributed-systems/listings")
)
from netsim import Net, Process  # noqa: E402

ELECTION, HEARTBEAT = (30, 60), 10


class Server(Process):
    def __init__(self, name, names, buggy_commit=False):
        super().__init__(name)
        self.names, self.buggy_commit = names, buggy_commit
        self.term, self.voted_for, self.log = 0, None, []  # persistent
        self.reset()

    def reset(self):  # volatile state: at the start and after a crash
        self.role, self.leader, self.commit, self.epoch = "follower", None, 0, 0
        self.votes, self.next, self.match = set(), {}, {}

    def say(self, text):
        self.net.notes.append(f"t={self.net.now:>3} {self.name} {text}")

    def others(self):
        return [n for n in self.names if n != self.name]

    def last(self):
        return len(self.log), (self.log[-1][0] if self.log else 0)

    def term_at(self, i):
        return self.log[i - 1][0] if i > 0 else 0

    def wait_election(self):
        self.epoch += 1
        self.set_timer(self.net.rng.randint(*ELECTION), ("election", self.epoch))

    def on_start(self):
        self.wait_election()

    def on_recover(self):
        self.reset()
        self.say(f"recovers in term {self.term} with {len(self.log)} entries")
        self.wait_election()

    def on_timer(self, what):
        kind, epoch = what
        if epoch != self.epoch:
            return  # a timer that was reset since
        if kind == "election" and self.role != "leader":
            self.term, self.voted_for, self.role = self.term + 1, self.name, "candidate"
            self.votes = {self.name}
            self.say(f"times out: candidate for term {self.term}")
            for n in self.others():
                self.send(n, ("vote?", self.term, *self.last()))
            self.wait_election()
        elif kind == "heartbeat" and self.role == "leader":
            self.replicate()

    def step_down(self, term):
        if term > self.term:
            self.term, self.voted_for = term, None
        if self.role != "follower":
            self.say(f"becomes follower in term {self.term}")
        self.role = "follower"
        self.wait_election()

    def on_message(self, src, msg):
        kind, term = msg[0], msg[1]
        if term > self.term:
            self.step_down(term)
        getattr(self, "on_" + kind.replace("?", "_q"))(src, *msg[1:])

    def on_vote_q(self, src, term, last_index, last_term):
        my_index, my_term = self.last()
        # the election restriction: the candidate's log is at least as up to date
        up_to_date = (last_term, last_index) >= (my_term, my_index)
        grant = term == self.term and self.voted_for in (None, src) and up_to_date
        if grant:
            self.voted_for = src
            self.wait_election()
        self.send(src, ("vote", self.term, grant))

    def on_vote(self, src, term, granted):
        if self.role != "candidate" or term != self.term or not granted:
            return
        self.votes.add(src)
        if len(self.votes) > len(self.names) // 2:
            self.role, self.leader = "leader", self.name
            self.say(
                f"leader of term {self.term}, votes {','.join(sorted(self.votes))}"
            )
            self.net.leaders.append((self.term, self.name))
            self.next = {n: len(self.log) + 1 for n in self.others()}
            self.match = {n: 0 for n in self.others()}
            self.replicate()

    def submit(self, command):
        """A client's command: only a leader accepts it."""
        if self.role != "leader" or not self.up:
            return False
        self.log.append((self.term, command))
        self.say(f"appends {command} at index {len(self.log)}")
        self.replicate()
        return True

    def replicate(self):
        for n in self.others():
            prev = self.next[n] - 1
            entries = self.log[prev:]
            self.send(
                n, ("append", self.term, prev, self.term_at(prev), entries, self.commit)
            )
        self.epoch += 1
        self.set_timer(HEARTBEAT, ("heartbeat", self.epoch))

    def on_append(self, src, term, prev, prev_term, entries, leader_commit):
        if term < self.term:
            self.send(src, ("appended", self.term, False, 0))
            return
        if self.role == "candidate":
            self.say(f"hears leader {src}: follower in term {self.term}")
        self.role, self.leader = "follower", src
        self.wait_election()
        if prev > len(self.log) or self.term_at(prev) != prev_term:
            # no entry at prev with the leader's term there: refuse
            self.send(src, ("appended", self.term, False, 0))
            return
        for k, entry in enumerate(entries, start=prev + 1):
            if k <= len(self.log) and self.log[k - 1][0] != entry[0]:
                del self.log[k - 1 :]  # a conflicting suffix is removed
            if k > len(self.log):
                self.log.append(entry)
        self.advance(min(leader_commit, prev + len(entries)))
        self.send(src, ("appended", self.term, True, prev + len(entries)))

    def on_appended(self, src, term, success, match):
        if self.role != "leader" or term != self.term:
            return
        if not success:
            self.next[src] = max(1, self.next[src] - 1)  # back up one entry and retry
            return
        self.match[src] = max(self.match[src], match)
        self.next[src] = self.match[src] + 1
        for i in range(len(self.log), self.commit, -1):
            copies = 1 + sum(m >= i for m in self.match.values())
            current = self.term_at(i) == self.term or self.buggy_commit
            if copies > len(self.names) // 2 and current:  # the commitment rule
                self.advance(i)
                break

    def advance(self, index):
        """Commit up to index; the simulator records every entry ever committed."""
        for i in range(self.commit + 1, index + 1):
            self.net.committed.setdefault(i, set()).add(self.log[i - 1])
        self.commit = max(self.commit, index)


def cluster(seed, n=5, buggy_commit=False, **net_args):
    net = Net(seed=seed, **net_args)
    net.notes, net.leaders, net.committed = [], [], {}
    names = [f"S{i}" for i in range(1, n + 1)]
    servers = [Server(m, names, buggy_commit) for m in names]
    net.add(*servers)
    return net, servers


def leader(servers):
    up = [s for s in servers if s.up and s.role == "leader"]
    return max(up, key=lambda s: s.term) if up else None


def show(net, servers):
    """The servers' logs as term:command, with role and commit index."""
    lines = [f"logs at t={net.now}"]
    for s in servers:
        entries = " ".join(f"{t}:{c}" for t, c in s.log)
        state = s.role if s.up else "down"
        lines.append(
            f"  {s.name} {state:<9} term={s.term} commit={s.commit}  {entries}"
        )
    return "\n".join(lines)
