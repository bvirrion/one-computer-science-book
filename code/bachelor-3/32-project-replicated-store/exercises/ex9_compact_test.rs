// Exercise 9: compact the log file. Replay needs only the last vote and the entries of
// the log as it stands; every overwritten entry and older vote can go.
#[path = "../listings/store/src/wal.rs"]
#[allow(dead_code)]
mod wal;
use wal::{encode, Record};

/// The state that replay reconstructs: (term, voted_for, log of (term, command)).
fn replay(records: &[Record]) -> (u64, u32, Vec<(u64, String)>) {
    let (mut term, mut vote, mut log) = (0, 0, Vec::new());
    for r in records {
        match r {
            Record::Vote { term: t, voted_for } => (term, vote) = (*t, *voted_for),
            Record::Entry { index, term: t, command } => {
                log.truncate(*index as usize - 1);
                log.push((*t, command.clone()));
            }
        }
    }
    (term, vote, log)
}

fn compact(records: &[Record]) -> Vec<Record> {
    let (term, voted_for, log) = replay(records);
    let mut out = vec![Record::Vote { term, voted_for }];
    for (i, (t, command)) in log.into_iter().enumerate() {
        out.push(Record::Entry { index: i as u64 + 1, term: t, command });
    }
    out
}

#[test]
fn compaction_keeps_the_state() {
    let mut records = Vec::new();
    for term in 1..=20u64 {
        records.push(Record::Vote { term, voted_for: (term % 3 + 1) as u32 });
        for k in 0..5 {
            // each term rewrites the log from index 2 * term on: older entries are replaced
            let index = 2 * term + k;
            records.push(Record::Entry { index, term, command: format!("SET k{k} {term}") });
        }
    }
    records.insert(0, Record::Entry { index: 1, term: 1, command: "NOOP".into() });
    let small = compact(&records);
    assert_eq!(replay(&small), replay(&records));
    let size = |rs: &[Record]| rs.iter().map(|r| encode(r).len()).sum::<usize>();
    assert_eq!((records.len(), small.len()), (121, 45));
    assert!(size(&small) * 2 < size(&records));
}
