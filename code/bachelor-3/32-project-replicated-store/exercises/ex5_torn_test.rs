// Exercise 5: a replay that trusts the length field's promise. It reads whatever bytes
// are there and skips the checksum, so a record torn by a crash comes back shortened.
#[path = "../listings/store/src/wal.rs"]
#[allow(dead_code)]
mod wal;
use wal::{encode, Record};

fn decode_all_buggy(bytes: &[u8]) -> Vec<Record> {
    let (mut records, mut at) = (Vec::new(), 0);
    while at + 8 <= bytes.len() {
        let len = u32::from_le_bytes(bytes[at..at + 4].try_into().unwrap()) as usize;
        let payload = &bytes[at + 8..(at + 8 + len).min(bytes.len())]; // BUG: may be short
        let p = payload;
        let record = match p.first() {
            Some(b'E') if p.len() >= 17 => Record::Entry {
                index: u64::from_le_bytes(p[1..9].try_into().unwrap()),
                term: u64::from_le_bytes(p[9..17].try_into().unwrap()),
                command: String::from_utf8_lossy(&p[17..]).into_owned(),
            },
            _ => break,
        };
        records.push(record);
        at += 8 + len;
    }
    records
}

fn file() -> (Vec<Record>, Vec<u8>) {
    let records = vec![
        Record::Entry { index: 1, term: 1, command: "SET bridge open".into() },
        Record::Entry { index: 2, term: 1, command: "SET bridge closed".into() },
    ];
    let bytes = records.iter().flat_map(encode).collect();
    (records, bytes)
}

#[test]
fn the_buggy_replay_invents_a_value() {
    let (_, bytes) = file();
    let torn = &bytes[..bytes.len() - 5];
    let got = decode_all_buggy(torn);
    assert_eq!(got.len(), 2);
    assert_eq!(got[1], Record::Entry { index: 2, term: 1, command: "SET bridge c".into() });
}

#[test]
fn the_fixed_replay_drops_the_torn_record() {
    let (records, bytes) = file();
    for cut in 0..=bytes.len() {
        let (got, good) = wal::decode_all(&bytes[..cut]);
        assert!(records.starts_with(&got), "cut {cut}");
        assert_eq!(good, got.iter().map(|r| encode(r).len()).sum::<usize>());
    }
    // the checksum alone also catches a flipped byte in the command, which no length can
    let mut bad = bytes.clone();
    let last = bad.len() - 1;
    bad[last] ^= 1;
    assert_eq!(wal::decode_all(&bad).0, records[..1]);
}
