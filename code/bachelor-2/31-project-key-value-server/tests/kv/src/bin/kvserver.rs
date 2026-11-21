//! The server as a program, for the tests that kill it: kvserver PORT LOG.
use kv::log::{Flush, Log};
use kv::server::{serve_pool, Shared};
use kv::store::Sharded;
use std::net::TcpListener;
use std::path::Path;
use std::sync::{Arc, Mutex};

fn main() -> std::io::Result<()> {
    let args: Vec<String> = std::env::args().collect();
    let (log, map, _) = Log::open(Path::new(&args[2]), Flush::EveryRecord)?;
    let shared = Arc::new(Shared { store: Box::new(Sharded::new(16, map)), log: Some(Mutex::new(log)) });
    let listener = TcpListener::bind(("127.0.0.1", args[1].parse::<u16>().unwrap()))?;
    serve_pool(listener, shared, 4)
}
