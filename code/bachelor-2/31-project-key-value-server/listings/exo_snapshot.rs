// capture: scratch
// exo_snapshot.rs (exercise 9): recovery = the latest snapshot, then the log written after it.
#[allow(dead_code)]
mod log;
#[allow(dead_code)]
mod protocol;
#[allow(dead_code)]
mod store;

use log::{replay, Flush, Log};
use protocol::Command;
use std::path::Path;

fn set(k: &str, v: &str) -> Command {
    Command::Set(k.to_string(), v.to_string())
}

/// The snapshot is a log of one SET per key: replay it, then the tail, as one log.
fn recover() -> std::io::Result<store::Map> {
    let mut bytes = std::fs::read("snapshot.log")?;
    bytes.extend(std::fs::read("tail.log")?);
    Ok(replay(&bytes).0)
}

fn main() -> std::io::Result<()> {
    let (mut log, _, _) = Log::open(Path::new("tail.log"), Flush::Never)?;
    for i in 0..1000 {
        log.append(&set(&format!("k{}", i % 10), &format!("v{i}")))?;
    }
    let map = replay(&std::fs::read("tail.log")?).0;
    // The snapshot: the map as one SET per key, written as a new file; the log starts again.
    let mut snapshot = Vec::new();
    let mut keys: Vec<_> = map.iter().collect();
    keys.sort();
    for (k, v) in keys {
        snapshot.extend(log::record(&set(k, v)));
    }
    std::fs::write("snapshot.tmp", &snapshot)?; // complete, then renamed: never torn
    std::fs::rename("snapshot.tmp", "snapshot.log")?;
    std::fs::write("tail.log", b"")?;
    let (mut log, _, _) = Log::open(Path::new("tail.log"), Flush::Never)?;
    log.append(&set("k3", "after"))?;
    log.append(&Command::Del("k4".to_string()))?;
    println!("snapshot: {} bytes; tail: {} bytes", snapshot.len(),
             std::fs::metadata("tail.log")?.len());
    let got = recover()?;
    println!("k3 = {:?}, k4 = {:?}, {} keys", got.get("k3"), got.get("k4"), got.len());
    Ok(())
}
