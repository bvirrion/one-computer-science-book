// Raft in the simulator: thousands of seeded runs with losses and crashes, every
// safety property checked; and the two faults the node must not have, caught.
use store::raft::{Msg, Output, Raft, Role};
use store::sim::{run, Settings};

#[test]
fn safe_under_loss_and_crashes() {
    let s = Settings::new(400, 50, 2);
    let (mut committed, mut elections) = (0, 0);
    for seed in 1..=2000 {
        let r = run(seed, &s);
        assert!(r.violations.is_empty(), "seed {seed}: {:?}", r.violations);
        committed += r.committed;
        elections += r.elections;
    }
    assert!(committed > 300_000 && elections > 2000);
}

#[test]
fn the_printed_summary() {
    let s = Settings::new(400, 50, 2);
    let rs: Vec<_> = (1..=1000).map(|seed| run(seed, &s)).collect();
    let crashes: usize = rs.iter().map(|r| r.crashes).sum();
    let elections: usize = rs.iter().map(|r| r.elections).sum();
    let committed: usize = rs.iter().map(|r| r.committed).sum();
    assert_eq!((crashes, elections, committed), (2217, 1699, 182_137)); // as m3_session prints
    assert!(rs.iter().all(|r| r.violations.is_empty()));
}

#[test]
fn faults_are_caught() {
    // Exercise 11: 2,000 seeds with 0.5 % crashes per tick; which runs break safety, and
    // which property each run breaks first
    for (forget, unsynced, runs, first, kind, of_kind) in [
        (true, false, 107, 21, "election safety", 106),
        (false, true, 18, 25, "leader completeness", 17),
    ] {
        let mut s = Settings::new(400, 50, 5);
        (s.forget_votes, s.lose_unsynced) = (forget, unsynced);
        let bad: Vec<(u64, String)> = (1..=2000)
            .filter_map(|seed| {
                run(seed, &s).violations.first().map(|v| (seed, v.clone()))
            })
            .collect();
        assert_eq!(
            (bad.len(), bad[0].0),
            (runs, first),
            "forget {forget}, unsynced {unsynced}"
        );
        assert_eq!(bad.iter().filter(|(_, v)| v.starts_with(kind)).count(), of_kind);
    }
    let s = Settings::new(400, 50, 5);
    assert!((1..=2000).all(|seed| run(seed, &s).violations.is_empty()));
}

/// Delivers every message until none is left; `cut` nodes neither send nor receive.
fn settle(rafts: &mut [Raft], mut queue: Vec<(u32, u32, Msg)>, cut: &[u32]) -> usize {
    let mut delivered = 0;
    while let Some((from, to, msg)) = (!queue.is_empty()).then(|| queue.remove(0)) {
        if cut.contains(&from) || cut.contains(&to) {
            continue;
        }
        delivered += 1;
        let mut out = Output::default();
        rafts[to as usize - 1].receive(from, msg, &mut out);
        queue.extend(out.send.into_iter().map(|(t, m)| (to, t, m)));
    }
    delivered
}

fn three() -> Vec<Raft> {
    (1..=3)
        .map(|id| {
            Raft::new(
                id,
                (1..=3).filter(|&p| p != id).collect(),
                &[],
                (10, 20),
                id as u64,
            )
        })
        .collect()
}

fn elect(rafts: &mut [Raft], id: u32, cut: &[u32]) {
    let mut out = Output::default();
    for _ in 0..20 {
        rafts[id as usize - 1].tick(&mut out);
        if !out.send.is_empty() {
            break;
        }
    }
    settle(rafts, out.send.into_iter().map(|(t, m)| (id, t, m)).collect(), cut);
    assert_eq!(rafts[id as usize - 1].role, Role::Leader);
}

#[test]
fn messages_per_write() {
    // Exercise 8: with three replicas and no loss, one write costs four messages.
    let mut rafts = three();
    elect(&mut rafts, 1, &[]);
    let mut out = Output::default();
    rafts[0].propose("SET a 1".into(), &mut out);
    let n = out.send.len()
        + settle(
            &mut rafts,
            out.send.into_iter().map(|(t, m)| (1, t, m)).collect(),
            &[],
        );
    assert_eq!(n, 2 + 4); // 2 appends sent, then 2 delivered and 2 answers delivered
    assert_eq!(rafts[0].commit, 2);
    assert_eq!(rafts[1].commit, 1); // the followers learn of the commit at the next append
}

#[test]
fn a_deposed_leader_reads_stale() {
    // Exercise 7: node 1 is cut off; 2 and 3 elect 2 and commit a new value, while
    // node 1 still believes it leads and its map still has the old one.
    let mut rafts = three();
    elect(&mut rafts, 1, &[]);
    let mut out = Output::default();
    rafts[0].propose("SET a 1".into(), &mut out);
    settle(&mut rafts, out.send.into_iter().map(|(t, m)| (1, t, m)).collect(), &[]);
    let mut out = Output::default();
    rafts[0].tick(&mut out);
    rafts[0].tick(&mut out);
    rafts[0].tick(&mut out); // a heartbeat carries the commit index
    settle(&mut rafts, out.send.into_iter().map(|(t, m)| (1, t, m)).collect(), &[]);
    elect(&mut rafts, 2, &[1]);
    let mut out = Output::default();
    rafts[1].propose("SET a 2".into(), &mut out);
    settle(&mut rafts, out.send.into_iter().map(|(t, m)| (2, t, m)).collect(), &[1]);
    assert_eq!(rafts[1].commit, 4);
    assert_eq!(rafts[0].role, Role::Leader); // still, in term 1
    assert_eq!(rafts[0].log.last().unwrap().command, "SET a 1");
    // A read index would ask for a heartbeat round: node 1's appends reach nobody.
    let mut out = Output::default();
    for _ in 0..3 {
        rafts[0].tick(&mut out);
    }
    assert_eq!(
        settle(
            &mut rafts,
            out.send.into_iter().map(|(t, m)| (1, t, m)).collect(),
            &[1]
        ),
        0
    );
}

#[test]
fn election_restriction() {
    // Exercise 3: a candidate whose log is behind gets no vote.
    let ahead = vec![store::wal::Record::Entry {
        index: 1,
        term: 2,
        command: "SET a 1".into(),
    }];
    let mut voter = Raft::new(3, vec![1, 2], &ahead, (10, 20), 3);
    let mut out = Output::default();
    voter.receive(
        1,
        Msg::RequestVote { term: 3, last_index: 5, last_term: 1 },
        &mut out,
    );
    assert_eq!(out.send.last().unwrap().1, Msg::Vote { term: 3, granted: false });
    voter.receive(
        2,
        Msg::RequestVote { term: 3, last_index: 1, last_term: 2 },
        &mut out,
    );
    assert_eq!(out.send.last().unwrap().1, Msg::Vote { term: 3, granted: true });
}

#[test]
fn exercise_3_who_can_lead() {
    // election terms of the entries: S1 1 1 2, S2 1 1 3, S3 1 1; S3 starts the elections
    use store::wal::Record;
    let logs: [&[u64]; 3] = [&[1, 1, 2], &[1, 1, 3], &[1, 1]];
    let records = |terms: &[u64]| -> Vec<Record> {
        let mut r = vec![Record::Vote { term: 3, voted_for: 0 }];
        r.extend(terms.iter().enumerate().map(|(i, &t)| Record::Entry {
            index: i as u64 + 1,
            term: t,
            command: format!("SET x {i}"),
        }));
        r
    };
    let mut winners = Vec::new();
    for candidate in 1..=3u32 {
        let (index, term) = (
            logs[candidate as usize - 1].len() as u64,
            *logs[candidate as usize - 1].last().unwrap(),
        );
        let mut granted = 1;
        for voter in (1..=3u32).filter(|&v| v != candidate) {
            let peers = (1..=3).filter(|&p| p != voter).collect();
            let mut raft = Raft::new(
                voter,
                peers,
                &records(logs[voter as usize - 1]),
                (10, 20),
                1,
            );
            let mut out = Output::default();
            raft.receive(
                candidate,
                Msg::RequestVote { term: 4, last_index: index, last_term: term },
                &mut out,
            );
            if out.send.last().unwrap().1 == (Msg::Vote { term: 4, granted: true }) {
                granted += 1;
            }
        }
        if granted >= 2 {
            winners.push(candidate);
        }
    }
    assert_eq!(winners, [1, 2]);
}
