// capture: scratch
// demo.rs: start the server on 127.0.0.1:44310, run a scripted client, read the log back.
#[allow(dead_code)]
mod client;
#[allow(dead_code)]
mod log;
#[allow(dead_code)]
mod protocol;
#[allow(dead_code)]
mod server;
#[allow(dead_code)]
mod store;

use log::{replay, Flush, Log};
use server::Shared;
use std::net::TcpListener;
use std::path::Path;
use std::sync::{Arc, Mutex};
use std::thread;

fn main() -> std::io::Result<()> {
    let (log, map, recovery) = Log::open(Path::new("kv.log"), Flush::EveryRecord)?;
    println!("started with {} keys from {} records", map.len(), recovery.records);
    let shared = Arc::new(Shared {
        store: Box::new(store::Sharded::new(16, map)),
        log: Some(Mutex::new(log)),
    });
    let listener = TcpListener::bind("127.0.0.1:44310")?;
    thread::spawn(move || server::serve_pool(listener, shared, 4));

    let mut c = client::Client::connect("127.0.0.1:44310")?;
    let script = [
        "SET loan:3 out", "SET member:55 Garden-Lane", "GET loan:3", "GET loan:4",
        "SET loan:3 returned", "GET loan:3", "DEL loan:4", "DEL member:55", "COUNT",
        "get loan:3", "SET loan:5", "COUNT now", "", "QUIT",
    ];
    for line in script {
        println!("> {line:<26} < {}", c.request(line)?);
    }

    let (map, recovery) = replay(&std::fs::read("kv.log")?);
    let mut keys: Vec<_> = map.into_iter().collect();
    keys.sort();
    println!("the log: {} records, {} bytes; replayed: {keys:?}", recovery.records,
             recovery.kept_bytes);
    Ok(())
}
