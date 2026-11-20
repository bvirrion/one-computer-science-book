// sim.rs: Raft's nodes in one process, on a simulated network with seeded delays,
// losses and crashes. Every run is a function of its seed; the safety properties of
// Raft are checked after every step.
use crate::raft::{Msg, Output, Raft, Role};
use crate::wal::Record;
use std::cmp::Reverse;
use std::collections::{BTreeMap, BinaryHeap};

pub struct Rng(u64);

impl Rng {
    pub fn new(seed: u64) -> Rng {
        Rng(seed)
    }
    pub fn next_u64(&mut self) -> u64 {
        self.0 = self.0.wrapping_add(0x9E37_79B9_7F4A_7C15); // splitmix64
        let mut z = self.0;
        z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
        z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
        z ^ (z >> 31)
    }
    pub fn below(&mut self, n: u64) -> u64 {
        self.next_u64() % n
    }
}

pub struct Settings {
    pub nodes: u32,
    pub ticks: u32,
    pub loss_permille: u64, // each message is lost with this probability
    pub crash_permille: u64, // each tick, a node crashes with this probability
    pub forget_votes: bool, // fault: a restarted node has lost its vote records
    pub lose_unsynced: bool, // fault: a crash loses the records of the node's last step
}

impl Settings {
    pub fn new(ticks: u32, loss_permille: u64, crash_permille: u64) -> Settings {
        Settings {
            nodes: 3,
            ticks,
            loss_permille,
            crash_permille,
            forget_votes: false,
            lose_unsynced: false,
        }
    }
}

#[derive(Debug, Default)]
pub struct Report {
    pub elections: usize, // leaders elected
    pub committed: usize, // distinct entries applied somewhere
    pub crashes: usize,
    pub violations: Vec<String>,
    pub events: Vec<String>, // what happened, for a printed transcript
}

struct Cluster {
    rafts: Vec<Option<Raft>>, // None: crashed
    disks: Vec<Vec<Record>>,  // what each node forced to its disk
    last_write: Vec<usize>,   // how many records each node's last step wrote
    down_until: Vec<u32>,
    queue: BinaryHeap<Reverse<(u32, u64, u32, u32)>>, // (time, seq, from, to); body in `bodies`
    bodies: BTreeMap<u64, Msg>,
    seq: u64,
    chosen: BTreeMap<u64, (u64, String)>, // index -> the entry applied there by anyone
    leaders: BTreeMap<u64, u32>,          // term -> its leader
    report: Report,
}

const TIMEOUTS: (u32, u32) = (10, 20);

impl Cluster {
    fn handle(
        &mut self,
        at: u32,
        node: u32,
        out: Output,
        was_leader: bool,
        rng: &mut Rng,
        s: &Settings,
    ) {
        let i = node as usize - 1;
        self.last_write[i] = out.persist.len();
        self.disks[i].extend(out.persist); // forced before anything is sent
        for (to, msg) in out.send {
            if rng.below(1000) < s.loss_permille {
                continue;
            }
            self.seq += 1;
            self.queue.push(Reverse((
                at + 1 + rng.below(3) as u32,
                self.seq,
                node,
                to,
            )));
            self.bodies.insert(self.seq, msg);
        }
        for (index, entry) in out.apply {
            match self.chosen.get(&index) {
                None => {
                    self.chosen.insert(index, (entry.term, entry.command));
                    self.report.committed += 1;
                }
                Some(c) if *c != (entry.term, entry.command.clone()) => {
                    self.report.violations.push(format!(
                        "state machine safety: node {node} applies another entry {index}"
                    ))
                }
                Some(_) => {}
            }
        }
        let raft = self.rafts[i].as_ref().unwrap();
        if raft.role == Role::Leader && !was_leader {
            self.report.elections += 1;
            self.report
                .events
                .push(format!("t={at:<4} node {node} leads term {}", raft.term));
            if let Some(other) = self.leaders.insert(raft.term, node) {
                self.report.violations.push(format!(
                    "election safety: term {} has leaders {other} and {node}",
                    raft.term
                ));
            }
            for (&index, (term, command)) in &self.chosen {
                if raft.term_at(index) != *term
                    || raft.log[index as usize - 1].command != *command
                {
                    self.report.violations.push(format!(
                        "leader completeness: node {node} lacks entry {index}"
                    ));
                }
            }
        }
    }
}

/// One run: the safety properties are checked as it goes, log matching at the end.
pub fn run(seed: u64, s: &Settings) -> Report {
    let mut rng = Rng::new(seed);
    let ids: Vec<u32> = (1..=s.nodes).collect();
    let peers =
        |id: u32| ids.iter().copied().filter(|&p| p != id).collect::<Vec<_>>();
    let mut c = Cluster {
        rafts: ids
            .iter()
            .map(|&id| Some(Raft::new(id, peers(id), &[], TIMEOUTS, rng.next_u64())))
            .collect(),
        disks: vec![Vec::new(); s.nodes as usize],
        last_write: vec![0; s.nodes as usize],
        down_until: vec![0; s.nodes as usize],
        queue: BinaryHeap::new(),
        bodies: BTreeMap::new(),
        seq: 0,
        chosen: BTreeMap::new(),
        leaders: BTreeMap::new(),
        report: Report::default(),
    };
    let mut next_command = 1;
    for now in 0..s.ticks {
        while let Some(&Reverse((at, seq, from, to))) = c.queue.peek() {
            if at > now {
                break;
            }
            c.queue.pop();
            let msg = c.bodies.remove(&seq).unwrap();
            if let Some(raft) = c.rafts[to as usize - 1].as_mut() {
                let (was, mut out) = (raft.role == Role::Leader, Output::default());
                raft.receive(from, msg, &mut out);
                c.handle(now, to, out, was, &mut rng, s);
            }
        }
        for &id in &ids {
            let i = id as usize - 1;
            if c.rafts[i].is_none() && now >= c.down_until[i] {
                if s.forget_votes {
                    c.disks[i].retain(|r| matches!(r, Record::Entry { .. }));
                }
                c.rafts[i] = Some(Raft::new(
                    id,
                    peers(id),
                    &c.disks[i],
                    TIMEOUTS,
                    rng.next_u64(),
                ));
                c.report.events.push(format!("t={now:<4} node {id} restarts"));
            } else if c.rafts[i].is_some() && rng.below(1000) < s.crash_permille {
                c.rafts[i] = None; // its volatile state is lost; its disk is not
                if s.lose_unsynced {
                    let keep = c.disks[i].len() - c.last_write[i];
                    c.disks[i].truncate(keep);
                }
                c.down_until[i] = now + 20 + rng.below(40) as u32;
                c.report.crashes += 1;
                c.report.events.push(format!("t={now:<4} node {id} crashes"));
                continue;
            }
            if let Some(raft) = c.rafts[i].as_mut() {
                let (was, mut out) = (raft.role == Role::Leader, Output::default());
                raft.tick(&mut out);
                if now % 2 == 0 && raft.role == Role::Leader {
                    raft.propose(
                        format!("SET k{} {}", next_command % 7, next_command),
                        &mut out,
                    );
                    next_command += 1;
                }
                c.handle(now, id, out, was, &mut rng, s);
            }
        }
    }
    check_log_matching(&c.rafts, &mut c.report);
    c.report
}

/// If two logs hold an entry of the same term at the same index, they agree up to it.
fn check_log_matching(rafts: &[Option<Raft>], report: &mut Report) {
    let logs: Vec<&Raft> = rafts.iter().flatten().collect();
    for (a, b) in logs.iter().zip(logs.iter().skip(1)) {
        let common = a.log.len().min(b.log.len());
        if let Some(i) = (0..common).rev().find(|&i| a.log[i].term == b.log[i].term) {
            if a.log[..=i] != b.log[..=i] {
                report.violations.push(format!(
                    "log matching: nodes {} and {} differ before {}",
                    a.id,
                    b.id,
                    i + 1
                ));
            }
        }
    }
}
