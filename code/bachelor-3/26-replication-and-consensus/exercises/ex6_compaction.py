"""Exercise 6: a Raft log that can be compacted. Entries up to base are replaced by a
snapshot of the state they produced (a dict here) and the term of the last of them;
indices keep their meaning. install() is what a follower does with a leader's
snapshot when the entries it needs have been compacted away on the leader."""


class CompactLog:
    def __init__(self):
        self.base, self.base_term, self.state, self.entries = 0, 0, {}, []

    def last(self):
        """(index, term) of the last entry, or of the snapshot if nothing follows it."""
        n = self.base + len(self.entries)
        return n, (self.entries[-1][0] if self.entries else self.base_term)

    def term_at(self, i):
        if i == self.base:
            return self.base_term
        if self.base < i <= self.last()[0]:
            return self.entries[i - self.base - 1][0]
        raise IndexError(f"index {i} is compacted or beyond the log")

    def append(self, term, command):
        self.entries.append((term, command))

    def matches(self, prev, prev_term):
        """The AppendEntries check; below the snapshot every entry is committed and so
        agrees with any leader's log."""
        if prev < self.base:
            return True
        return prev <= self.last()[0] and self.term_at(prev) == prev_term

    def compact(self, upto):
        """Apply the entries up to upto (committed) to the state, then drop them."""
        if upto <= self.base:
            return
        term = self.term_at(upto)
        for _, (key, value) in self.entries[: upto - self.base]:
            self.state[key] = value
        self.entries = self.entries[upto - self.base :]
        self.base, self.base_term = upto, term

    def install(self, base, base_term, state):
        """A leader's snapshot: keep later entries only if the log agrees at base."""
        if base <= self.base:
            return
        keep = base <= self.last()[0] and self.term_at(base) == base_term
        self.entries = self.entries[base - self.base :] if keep else []
        self.base, self.base_term, self.state = base, base_term, dict(state)
