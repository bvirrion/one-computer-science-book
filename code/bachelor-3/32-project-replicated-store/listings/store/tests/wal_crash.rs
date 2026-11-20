// The log under a crash at every byte: whatever prefix of the file survives, replay
// returns exactly the records wholly inside it, cuts the rest, and appends after them.
use std::path::PathBuf;
use store::wal::{decode_all, encode, Record, Wal};

fn records() -> Vec<Record> {
    vec![
        Record::Vote { term: 1, voted_for: 1 },
        Record::Entry { index: 1, term: 1, command: "NOOP".into() },
        Record::Entry { index: 2, term: 1, command: "SET a 1".into() },
        Record::Vote { term: 2, voted_for: 3 },
        Record::Entry { index: 2, term: 2, command: "SET b héllo".into() },
        Record::Entry { index: 3, term: 2, command: "DEL a".into() },
    ]
}

fn scratch(name: &str) -> PathBuf {
    let dir =
        std::env::temp_dir().join(format!("store-wal-{}-{name}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    dir.join("wal.log")
}

#[test]
fn crash_at_every_byte() {
    let all = records();
    let bytes: Vec<u8> = all.iter().flat_map(encode).collect();
    let ends: Vec<usize> = all
        .iter()
        .scan(0, |at, r| {
            *at += encode(r).len();
            Some(*at)
        })
        .collect();
    let path = scratch("cut");
    for cut in 0..=bytes.len() {
        std::fs::write(&path, &bytes[..cut]).unwrap();
        let (mut wal, got) = Wal::open(&path).unwrap();
        let whole = ends.iter().filter(|&&e| e <= cut).count();
        assert_eq!(got, all[..whole], "cut at byte {cut}");
        let good = if whole == 0 { 0 } else { ends[whole - 1] };
        assert_eq!(
            std::fs::metadata(&path).unwrap().len() as usize,
            good,
            "torn tail cut off"
        );
        let extra = Record::Vote { term: 9, voted_for: 2 };
        wal.append(std::slice::from_ref(&extra)).unwrap();
        let (_, again) = Wal::open(&path).unwrap();
        assert_eq!(again.last(), Some(&extra));
        assert_eq!(again.len(), whole + 1);
    }
    std::fs::remove_dir_all(path.parent().unwrap()).unwrap();
}

#[test]
fn every_flipped_byte_stops_replay_at_its_record() {
    let all = records();
    let bytes: Vec<u8> = all.iter().flat_map(encode).collect();
    let mut start = 0;
    for (k, r) in all.iter().enumerate() {
        let len = encode(r).len();
        for at in start..start + len {
            let mut bad = bytes.clone();
            bad[at] ^= 0x10;
            let (got, good) = decode_all(&bad);
            // a changed length may still frame a record only if the checksum agrees: never here
            assert_eq!(got, all[..k], "byte {at} flipped");
            assert_eq!(good, start);
        }
        start += len;
    }
}

#[test]
fn crc32_check_value() {
    assert_eq!(store::wal::crc32(b"123456789"), 0xCBF4_3926); // the standard check value
    assert_eq!(
        encode(&Record::Entry { index: 2, term: 1, command: "SET a 1".into() }).len(),
        8 + 17 + 7
    );
    assert_eq!(encode(&Record::Vote { term: 1, voted_for: 1 }).len(), 8 + 13);
}

#[test]
fn exercise_2_a_crash_after_100_bytes() {
    // the session's file: a vote, the no-op, SET bridge open, SET bridge closed
    let all = [
        Record::Vote { term: 1, voted_for: 1 },
        Record::Entry { index: 1, term: 1, command: "NOOP".into() },
        Record::Entry { index: 2, term: 1, command: "SET bridge open".into() },
        Record::Entry { index: 3, term: 1, command: "SET bridge closed".into() },
    ];
    let bytes: Vec<u8> = all.iter().flat_map(encode).collect();
    assert_eq!(bytes.len(), 132);
    let sizes: Vec<usize> = all.iter().map(|r| encode(r).len()).collect();
    assert_eq!(sizes, [21, 29, 40, 42]);
    let (got, good) = decode_all(&bytes[..100]);
    assert_eq!((got.len(), good), (3, 90));
}
