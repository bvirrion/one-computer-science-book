// raft.rs: Raft as a pure state machine. It never reads a clock, a socket or a file:
// time comes in as ticks, messages as calls, and every call returns what to force to
// the disk, what to send, and which entries are newly committed.
use crate::wal::Record;
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Entry {
    pub term: u64,
    pub command: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Msg {
    RequestVote {
        term: u64,
        last_index: u64,
        last_term: u64,
    },
    Vote {
        term: u64,
        granted: bool,
    },
    Append {
        term: u64,
        prev_index: u64,
        prev_term: u64,
        entries: Vec<Entry>,
        commit: u64,
    },
    Appended {
        term: u64,
        success: bool,
        match_index: u64,
    },
}

impl Msg {
    pub fn term(&self) -> u64 {
        match self {
            Msg::RequestVote { term, .. } | Msg::Vote { term, .. } => *term,
            Msg::Append { term, .. } | Msg::Appended { term, .. } => *term,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Role {
    Follower,
    Candidate,
    Leader,
}

/// What one call asks of the node: first force `persist` to the disk, then send.
#[derive(Debug, Default)]
pub struct Output {
    pub persist: Vec<Record>,
    pub send: Vec<(u32, Msg)>,
    pub apply: Vec<(u64, Entry)>, // newly committed entries, in index order
}

pub const HEARTBEAT: u32 = 3; // ticks between a leader's appends
pub const MAX_BATCH: usize = 64; // entries per append message

pub struct Raft {
    pub id: u32,
    peers: Vec<u32>,
    pub term: u64,
    voted_for: u32,      // 0: nobody in this term
    pub log: Vec<Entry>, // log[i - 1] is the entry at index i
    pub commit: u64,
    applied: u64,
    pub role: Role,
    pub leader: u32, // 0: not known
    votes: Vec<u32>,
    next: BTreeMap<u32, u64>,
    matched: BTreeMap<u32, u64>,
    elapsed: u32,
    timeout: u32,
    timeouts: (u32, u32), // an election timeout is drawn in [lo, hi) ticks
    rng: u64,
}

impl Raft {
    /// A node starting, or restarting after a crash, from the records of its log.
    pub fn new(
        id: u32,
        peers: Vec<u32>,
        records: &[Record],
        timeouts: (u32, u32),
        seed: u64,
    ) -> Raft {
        let mut r = Raft {
            id,
            peers,
            term: 0,
            voted_for: 0,
            log: Vec::new(),
            commit: 0,
            applied: 0,
            role: Role::Follower,
            leader: 0,
            votes: Vec::new(),
            next: BTreeMap::new(),
            matched: BTreeMap::new(),
            elapsed: 0,
            timeout: 0,
            timeouts,
            rng: seed | 1,
        };
        for record in records {
            match record {
                Record::Vote { term, voted_for } => {
                    (r.term, r.voted_for) = (*term, *voted_for)
                }
                Record::Entry { index, term, command } => {
                    r.log.truncate(*index as usize - 1); // a later entry replaces a suffix
                    r.log.push(Entry { term: *term, command: command.clone() });
                }
            }
        }
        r.reset_timer();
        r
    }

    fn reset_timer(&mut self) {
        self.rng ^= self.rng << 13; // xorshift64
        self.rng ^= self.rng >> 7;
        self.rng ^= self.rng << 17;
        let (lo, hi) = self.timeouts;
        self.timeout = lo + (self.rng % (hi - lo) as u64) as u32;
        self.elapsed = 0;
    }

    fn majority(&self) -> usize {
        let cluster = self.peers.len() + 1;
        cluster / 2 + 1
    }

    pub fn last(&self) -> (u64, u64) {
        (self.log.len() as u64, self.term_at(self.log.len() as u64))
    }

    pub fn term_at(&self, index: u64) -> u64 {
        match index {
            0 => 0,
            i => self.log.get(i as usize - 1).map_or(0, |e| e.term),
        }
    }

    pub fn tick(&mut self, out: &mut Output) {
        self.elapsed += 1;
        if self.role == Role::Leader {
            if self.elapsed >= HEARTBEAT {
                self.replicate(out);
            }
        } else if self.elapsed >= self.timeout {
            self.start_election(out);
        }
    }

    fn start_election(&mut self, out: &mut Output) {
        self.term += 1;
        (self.role, self.voted_for, self.leader) = (Role::Candidate, self.id, 0);
        self.votes = vec![self.id];
        out.persist.push(Record::Vote { term: self.term, voted_for: self.id });
        self.reset_timer();
        if self.votes.len() >= self.majority() {
            return self.become_leader(out); // a cluster of one
        }
        let (last_index, last_term) = self.last();
        for &p in &self.peers {
            out.send.push((
                p,
                Msg::RequestVote { term: self.term, last_index, last_term },
            ));
        }
    }

    fn become_leader(&mut self, out: &mut Output) {
        (self.role, self.leader) = (Role::Leader, self.id);
        for &p in &self.peers {
            self.next.insert(p, self.log.len() as u64 + 1);
            self.matched.insert(p, 0);
        }
        // An entry of the new term, so that the entries before it can be committed.
        self.propose("NOOP".to_string(), out);
    }

    fn step_down(&mut self, term: u64, out: &mut Output) {
        if term > self.term {
            (self.term, self.voted_for, self.leader) = (term, 0, 0);
            out.persist.push(Record::Vote { term, voted_for: 0 });
        }
        self.role = Role::Follower;
        self.reset_timer();
    }

    /// A client's command: only a leader takes it. Returns its index in the log.
    pub fn propose(&mut self, command: String, out: &mut Output) -> Option<u64> {
        if self.role != Role::Leader {
            return None;
        }
        self.log.push(Entry { term: self.term, command: command.clone() });
        let index = self.log.len() as u64;
        out.persist.push(Record::Entry { index, term: self.term, command });
        self.advance_leader_commit(out);
        self.replicate(out);
        Some(index)
    }

    fn replicate(&mut self, out: &mut Output) {
        for p in self.peers.clone() {
            self.send_append(p, out);
        }
        self.elapsed = 0;
    }

    fn send_append(&self, peer: u32, out: &mut Output) {
        let prev_index = self.next[&peer] - 1;
        let end = self.log.len().min(prev_index as usize + MAX_BATCH);
        let entries = self.log[prev_index as usize..end].to_vec();
        let prev_term = self.term_at(prev_index);
        out.send.push((
            peer,
            Msg::Append {
                term: self.term,
                prev_index,
                prev_term,
                entries,
                commit: self.commit,
            },
        ));
    }

    pub fn receive(&mut self, from: u32, msg: Msg, out: &mut Output) {
        if msg.term() > self.term {
            self.step_down(msg.term(), out);
        }
        match msg {
            Msg::RequestVote { term, last_index, last_term } => {
                // the election restriction: the candidate's log is as up to date
                let up_to_date =
                    (last_term, last_index) >= (self.last().1, self.last().0);
                let free = self.voted_for == 0 || self.voted_for == from;
                let granted = term == self.term && free && up_to_date;
                if granted && self.voted_for != from {
                    self.voted_for = from;
                    out.persist.push(Record::Vote { term, voted_for: from });
                }
                if granted {
                    self.reset_timer();
                }
                out.send.push((from, Msg::Vote { term: self.term, granted }));
            }
            Msg::Vote { term, granted } => {
                if self.role == Role::Candidate
                    && term == self.term
                    && granted
                    && !self.votes.contains(&from)
                {
                    self.votes.push(from);
                    if self.votes.len() >= self.majority() {
                        self.become_leader(out);
                    }
                }
            }
            Msg::Append { term, prev_index, prev_term, entries, commit } => self
                .on_append(from, term, prev_index, prev_term, entries, commit, out),
            Msg::Appended { term, success, match_index } => {
                if self.role != Role::Leader || term != self.term {
                    return;
                }
                if success {
                    let m = self.matched[&from].max(match_index);
                    self.matched.insert(from, m);
                    self.next.insert(from, m + 1);
                    self.advance_leader_commit(out);
                    if m < self.log.len() as u64 {
                        self.send_append(from, out); // more than one message held
                    }
                } else {
                    let next = (self.next[&from] - 1).min(match_index + 1).max(1);
                    self.next.insert(from, next);
                    self.send_append(from, out);
                }
            }
        }
    }

    #[allow(clippy::too_many_arguments)]
    fn on_append(
        &mut self,
        from: u32,
        term: u64,
        prev_index: u64,
        prev_term: u64,
        entries: Vec<Entry>,
        commit: u64,
        out: &mut Output,
    ) {
        if term < self.term {
            out.send.push((
                from,
                Msg::Appended { term: self.term, success: false, match_index: 0 },
            ));
            return;
        }
        (self.role, self.leader) = (Role::Follower, from);
        self.reset_timer();
        if prev_index > self.log.len() as u64 || self.term_at(prev_index) != prev_term
        {
            // no entry at prev_index with the leader's term: refuse, with a hint
            let hint = (self.log.len() as u64).min(prev_index.saturating_sub(1));
            out.send.push((
                from,
                Msg::Appended { term, success: false, match_index: hint },
            ));
            return;
        }
        let count = entries.len() as u64;
        for (k, entry) in (prev_index + 1..).zip(entries) {
            if k <= self.log.len() as u64 && self.term_at(k) != entry.term {
                self.log.truncate(k as usize - 1); // a conflicting suffix is removed
            }
            if k > self.log.len() as u64 {
                let record = Record::Entry {
                    index: k,
                    term: entry.term,
                    command: entry.command.clone(),
                };
                out.persist.push(record);
                self.log.push(entry);
            }
        }
        let new_commit = commit.min(prev_index + count);
        if new_commit > self.commit {
            self.commit = new_commit;
            self.apply(out);
        }
        out.send.push((
            from,
            Msg::Appended { term, success: true, match_index: prev_index + count },
        ));
    }

    /// The commitment rule: an entry of the current term held by a majority is
    /// committed, and every entry before it with it.
    fn advance_leader_commit(&mut self, out: &mut Output) {
        for i in (self.commit + 1..=self.log.len() as u64).rev() {
            let copies = 1 + self.matched.values().filter(|&&m| m >= i).count();
            if self.term_at(i) == self.term && copies >= self.majority() {
                self.commit = i;
                self.apply(out);
                break;
            }
        }
    }

    fn apply(&mut self, out: &mut Output) {
        while self.applied < self.commit {
            self.applied += 1;
            out.apply
                .push((self.applied, self.log[self.applied as usize - 1].clone()));
        }
    }
}
