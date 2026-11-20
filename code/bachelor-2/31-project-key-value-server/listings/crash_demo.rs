// capture: scratch
// crash_demo.rs: a torn last record, a zeroed tail and a flipped bit, each recovered.
#[allow(dead_code)]
mod log;
#[allow(dead_code)]
mod protocol;
#[allow(dead_code)]
mod store;

use log::{record, Flush, Log};
use protocol::Command;
use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::Path;

fn set(k: &str, v: &str) -> Command {
    Command::Set(k.to_string(), v.to_string())
}

fn restart(path: &Path, what: &str) -> std::io::Result<()> {
    let (_, map, r) = Log::open(path, Flush::EveryRecord)?;
    let mut keys: Vec<_> = map.into_iter().collect();
    keys.sort();
    let s = if r.records == 1 { "" } else { "s" };
    println!("{what:<26} {} record{s} kept, {:>2} bytes dropped: {keys:?}", r.records,
             r.dropped_bytes);
    Ok(())
}

fn main() -> std::io::Result<()> {
    let path = Path::new("kv.log");
    let (mut log, _, _) = Log::open(path, Flush::EveryRecord)?;
    for (k, v) in [("a", "1"), ("b", "2"), ("a", "3")] {
        log.append(&set(k, v))?;
    }
    drop(log);
    println!("three records: {} bytes", fs::metadata(path)?.len());

    // The crash: only the first 11 of the 4th record's 15 bytes reached the file.
    let torn = record(&set("c", "4"));
    OpenOptions::new().append(true).open(path)?.write_all(&torn[..11])?;
    restart(path, "torn last record:")?;
    println!("after the restart the file has {} bytes again", fs::metadata(path)?.len());

    // A file system may leave zeros after a crash: len 0 and CRC 0 look valid.
    OpenOptions::new().append(true).open(path)?.write_all(&[0u8; 16])?;
    restart(path, "zeroed tail:")?;

    // A bit flipped in the value of the 2nd record: its CRC no longer matches.
    let mut bytes = fs::read(path)?;
    bytes[15 + 14] ^= 0x01;
    fs::write(path, &bytes)?;
    restart(path, "flipped bit in record 2:")?;
    Ok(())
}
