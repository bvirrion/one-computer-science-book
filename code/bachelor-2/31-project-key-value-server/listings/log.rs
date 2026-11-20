// log.rs: the append-only log. A record is len (4 bytes) | crc32 (4 bytes) | command.
use crate::protocol::{parse, Command, MAX_LINE};
use crate::store::Map;
use std::fs::{self, File, OpenOptions};
use std::io::{self, Write};
use std::path::{Path, PathBuf};

/// The CRC-32 of zlib and Ethernet, bit by bit: reflected, pre- and post-complemented.
pub fn crc32(data: &[u8]) -> u32 {
    let mut crc = 0xFFFF_FFFFu32;
    for &byte in data {
        crc ^= byte as u32;
        for _ in 0..8 {
            crc = if crc & 1 == 1 { (crc >> 1) ^ 0xEDB8_8320 } else { crc >> 1 };
        }
    }
    !crc
}

pub fn record(cmd: &Command) -> Vec<u8> {
    let payload = cmd.to_string().into_bytes();
    let mut out = Vec::with_capacity(8 + payload.len());
    out.extend_from_slice(&(payload.len() as u32).to_le_bytes());
    out.extend_from_slice(&crc32(&payload).to_le_bytes());
    out.extend_from_slice(&payload);
    out
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Flush {
    /// sync_data after every record: a reply OK means the record is on the disk.
    EveryRecord,
    /// leave the record to the operating system, which writes it out later.
    Never,
}

#[derive(Debug, PartialEq, Eq)]
pub struct Recovery {
    pub records: usize,
    pub kept_bytes: u64,
    pub dropped_bytes: u64,
}

/// Rebuild the map from the bytes of a log; stop at the first record that is
/// short, fails its CRC or does not parse, and drop everything from there.
pub fn replay(bytes: &[u8]) -> (Map, Recovery) {
    let mut map = Map::new();
    let (mut at, mut records) = (0usize, 0usize);
    while let Some((cmd, size)) = next_record(&bytes[at..]) {
        match &cmd {
            Command::Set(k, v) => map.insert(k.clone(), v.clone()),
            Command::Del(k) => map.remove(k),
            _ => unreachable!("next_record returns SET and DEL only"),
        };
        at += size;
        records += 1;
    }
    let dropped = (bytes.len() - at) as u64;
    (map, Recovery { records, kept_bytes: at as u64, dropped_bytes: dropped })
}

fn next_record(b: &[u8]) -> Option<(Command, usize)> {
    let len = u32::from_le_bytes(b.get(0..4)?.try_into().ok()?) as usize;
    let crc = u32::from_le_bytes(b.get(4..8)?.try_into().ok()?);
    let payload = b.get(8..8 + len.min(MAX_LINE + 1))?;
    if payload.len() != len || crc32(payload) != crc {
        return None;
    }
    match parse(std::str::from_utf8(payload).ok()?) {
        Ok(cmd @ (Command::Set(..) | Command::Del(_))) => Some((cmd, 8 + len)),
        _ => None, // a zeroed tail has len 0 and the CRC of nothing, 0: it fails here
    }
}

pub struct Log {
    path: PathBuf,
    file: File,
    policy: Flush,
}

impl Log {
    /// Replay the log at path, cut off a torn tail, and open it for appending.
    pub fn open(path: &Path, policy: Flush) -> io::Result<(Log, Map, Recovery)> {
        let bytes = fs::read(path).or_else(|e| match e.kind() {
            io::ErrorKind::NotFound => Ok(Vec::new()),
            _ => Err(e),
        })?;
        let (map, recovery) = replay(&bytes);
        let file = OpenOptions::new().create(true).append(true).open(path)?;
        file.set_len(recovery.kept_bytes)?;
        file.sync_all()?;
        Ok((Log { path: path.to_path_buf(), file, policy }, map, recovery))
    }

    pub fn append(&mut self, cmd: &Command) -> io::Result<()> {
        self.file.write_all(&record(cmd))?;
        if self.policy == Flush::EveryRecord {
            self.file.sync_data()?;
        }
        Ok(())
    }

    /// Compaction: write one SET per key, sorted, to a new file, make it durable,
    /// and rename it over the log; a crash leaves either the old log or the new one.
    pub fn rewrite(&mut self, maps: &[&Map]) -> io::Result<u64> {
        let mut entries: Vec<(&String, &String)> =
            maps.iter().flat_map(|m| m.iter()).collect();
        entries.sort();
        let tmp = self.path.with_extension("compacting");
        let mut out = File::create(&tmp)?;
        let mut size = 0u64;
        for (k, v) in entries {
            let rec = record(&Command::Set(k.clone(), v.clone()));
            out.write_all(&rec)?;
            size += rec.len() as u64;
        }
        out.sync_all()?;
        fs::rename(&tmp, &self.path)?;
        let dir = self.path.parent().filter(|d| !d.as_os_str().is_empty());
        File::open(dir.unwrap_or(Path::new(".")))?.sync_all()?; // the rename itself
        self.file = OpenOptions::new().append(true).open(&self.path)?;
        Ok(size)
    }
}
