// exo_log_size.rs (exercise 4): the log after n SETs over k keys, before and after compaction.
#[allow(dead_code)]
mod log;
#[allow(dead_code)]
mod protocol;
#[allow(dead_code)]
mod store;

use protocol::Command;
use store::Map;

fn main() {
    println!("       n      k   log (bytes)   compacted (bytes)");
    for (n, k) in [(1000, 10), (1000, 1000), (100_000, 10), (100_000, 1000)] {
        let (mut size, mut map) = (0, Map::new());
        for i in 0..n {
            // keys k000..k999 and values v00000..v99999: fixed widths
            let cmd = Command::Set(format!("k{:03}", i % k), format!("v{i:05}"));
            size += log::record(&cmd).len();
            if let Command::Set(key, value) = cmd {
                map.insert(key, value);
            }
        }
        let compacted: usize = map.iter()
            .map(|(key, v)| log::record(&Command::Set(key.clone(), v.clone())).len())
            .sum();
        println!("{n:>8} {k:>6} {size:>13} {compacted:>19}");
    }
}
