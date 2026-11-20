// wal.rs: the write-ahead log. Every change to the state Raft must keep across a crash
// is a record appended to one file and forced to the disk before anyone is told of it.
// Record: length (u32, little-endian) | CRC-32 of the payload (u32) | payload.
// Payload: b'V' term (u64) voted_for (u32, 0 = nobody)
//        | b'E' index (u64) term (u64) command (UTF-8, the rest of the payload).
use std::fs::{File, OpenOptions};
use std::io::{self, Read, Write};
use std::path::Path;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Record {
    Vote { term: u64, voted_for: u32 },
    Entry { index: u64, term: u64, command: String },
}

/// CRC-32 (IEEE 802.3, reflected, polynomial 0xEDB88320), bit by bit.
pub fn crc32(bytes: &[u8]) -> u32 {
    let mut crc = !0u32;
    for &b in bytes {
        crc ^= b as u32;
        for _ in 0..8 {
            crc = if crc & 1 == 1 { (crc >> 1) ^ 0xEDB8_8320 } else { crc >> 1 };
        }
    }
    !crc
}

pub fn encode(record: &Record) -> Vec<u8> {
    let mut payload = Vec::new();
    match record {
        Record::Vote { term, voted_for } => {
            payload.push(b'V');
            payload.extend(term.to_le_bytes());
            payload.extend(voted_for.to_le_bytes());
        }
        Record::Entry { index, term, command } => {
            payload.push(b'E');
            payload.extend(index.to_le_bytes());
            payload.extend(term.to_le_bytes());
            payload.extend(command.as_bytes());
        }
    }
    let mut out = (payload.len() as u32).to_le_bytes().to_vec();
    out.extend(crc32(&payload).to_le_bytes());
    out.extend(payload);
    out
}

fn decode_payload(p: &[u8]) -> Option<Record> {
    let u64_at =
        |i: usize| Some(u64::from_le_bytes(p.get(i..i + 8)?.try_into().ok()?));
    match p.first()? {
        b'V' if p.len() == 13 => Some(Record::Vote {
            term: u64_at(1)?,
            voted_for: u32::from_le_bytes(p[9..13].try_into().ok()?),
        }),
        b'E' if p.len() >= 17 => Some(Record::Entry {
            index: u64_at(1)?,
            term: u64_at(9)?,
            command: String::from_utf8(p[17..].to_vec()).ok()?,
        }),
        _ => None,
    }
}

/// The records of a log file's bytes, up to the first one that is cut short or whose
/// checksum fails, and the length of the good prefix.
pub fn decode_all(bytes: &[u8]) -> (Vec<Record>, usize) {
    let (mut records, mut at) = (Vec::new(), 0);
    while let Some(header) = bytes.get(at..at + 8) {
        let len = u32::from_le_bytes(header[0..4].try_into().unwrap()) as usize;
        let crc = u32::from_le_bytes(header[4..8].try_into().unwrap());
        let Some(payload) = bytes.get(at + 8..at + 8 + len) else {
            break;
        };
        if crc32(payload) != crc {
            break;
        }
        let Some(record) = decode_payload(payload) else {
            break;
        };
        records.push(record);
        at += 8 + len;
    }
    (records, at)
}

pub struct Wal {
    file: File,
}

impl Wal {
    /// Opens (or creates) the log, returns its good records, and cuts off a torn tail
    /// so that the next record is appended right after the last good one.
    pub fn open(path: &Path) -> io::Result<(Wal, Vec<Record>)> {
        let mut file =
            OpenOptions::new().read(true).append(true).create(true).open(path)?;
        let mut bytes = Vec::new();
        file.read_to_end(&mut bytes)?;
        let (records, good) = decode_all(&bytes);
        if good < bytes.len() {
            file.set_len(good as u64)?;
            file.sync_all()?;
        }
        Ok((Wal { file }, records))
    }

    /// Appends the records and forces them to the disk: one write, one fsync.
    pub fn append(&mut self, records: &[Record]) -> io::Result<()> {
        if records.is_empty() {
            return Ok(());
        }
        let bytes: Vec<u8> = records.iter().flat_map(encode).collect();
        self.file.write_all(&bytes)?;
        self.file.sync_all()
    }
}
