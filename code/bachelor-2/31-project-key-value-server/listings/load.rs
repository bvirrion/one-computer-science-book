// capture: scratch timeout=300
// load.rs: one lock against 16 shards, in process and over TCP; the cost of syncing the log.
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

use protocol::Command;
use server::Shared;
use std::net::TcpListener;
use std::path::Path;
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Instant;

/// A seeded generator: the same workload on every run.
struct Lcg(u64);
impl Lcg {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        self.0 >> 33
    }
    /// 90 % GET, 10 % SET, over 1000 keys.
    fn command(&mut self) -> Command {
        let key = format!("k{}", self.next() % 1000);
        if self.next() % 10 == 0 {
            Command::Set(key, "v".to_string())
        } else {
            Command::Get(key)
        }
    }
}

fn store(sharded: bool) -> Box<dyn store::Store> {
    if sharded {
        Box::new(store::Sharded::new(16, store::Map::new()))
    } else {
        Box::new(store::OneLock::new(store::Map::new()))
    }
}

/// Millions of operations per second, `threads` threads calling the store directly.
fn in_process(sharded: bool, threads: u64, ops: u64) -> f64 {
    let s: Arc<dyn store::Store> = Arc::from(store(sharded));
    let start = Instant::now();
    let workers: Vec<_> = (0..threads).map(|t| {
        let s = Arc::clone(&s);
        thread::spawn(move || {
            let mut rng = Lcg(t + 1);
            for _ in 0..ops {
                s.apply(&rng.command(), None);
            }
        })
    }).collect();
    workers.into_iter().for_each(|w| w.join().unwrap());
    (threads * ops) as f64 / start.elapsed().as_secs_f64() / 1e6
}

/// Thousands of requests per second over TCP, and the latency percentiles in µs.
fn over_tcp(addr: &str, clients: u64, requests: u64) -> (f64, f64, f64) {
    let start = Instant::now();
    let workers: Vec<_> = (0..clients).map(|t| {
        let addr = addr.to_string();
        thread::spawn(move || {
            let (mut rng, mut c) = (Lcg(t + 1), client::Client::connect(&addr).unwrap());
            let mut times = Vec::with_capacity(requests as usize);
            for _ in 0..requests {
                let line = rng.command().to_string();
                let sent = Instant::now();
                c.request(&line).unwrap();
                times.push(sent.elapsed().as_secs_f64() * 1e6);
            }
            c.request("QUIT").unwrap();
            times
        })
    }).collect();
    let mut all: Vec<f64> = workers.into_iter().flat_map(|w| w.join().unwrap()).collect();
    let rate = all.len() as f64 / start.elapsed().as_secs_f64() / 1e3;
    all.sort_by(|a, b| a.total_cmp(b));
    let pct = |p: f64| all[((all.len() - 1) as f64 * p) as usize];
    (rate, pct(0.50), pct(0.99))
}

fn start(port: u16, sharded: bool, log: Option<log::Log>) -> String {
    let shared = Arc::new(Shared { store: store(sharded), log: log.map(Mutex::new) });
    let listener = TcpListener::bind(("127.0.0.1", port)).unwrap();
    thread::spawn(move || server::serve_pool(listener, shared, 8));
    format!("127.0.0.1:{port}")
}

fn main() {
    println!("in process: 400000 operations per thread, 90 % GET, 1000 keys (M ops/s)");
    println!("threads  one lock  16 shards");
    for threads in [1, 2, 4, 8] {
        let one = in_process(false, threads, 400_000);
        let many = in_process(true, threads, 400_000);
        println!("{threads:>7} {one:>9.2} {many:>10.2}");
    }
    println!("over TCP: 8 workers, 20000 requests per client (k req/s; p50, p99 in us)");
    println!("clients  one lock    p50    p99  16 shards    p50    p99");
    let (one, many) = (start(44314, false, None), start(44315, true, None));
    for clients in [1, 2, 4, 8] {
        let (r1, a1, b1) = over_tcp(&one, clients, 20_000);
        let (r2, a2, b2) = over_tcp(&many, clients, 20_000);
        println!("{clients:>7} {r1:>9.1} {a1:>6.0} {b1:>6.0} {r2:>10.1} {a2:>6.0} {b2:>6.0}");
    }
    println!("SET with the log, one client, 2000 requests (k req/s)");
    for (port, policy, name) in [(44316, log::Flush::EveryRecord, "sync every record"),
                                 (44317, log::Flush::Never, "leave it to the OS")] {
        let (log, _, _) = log::Log::open(Path::new(&format!("{port}.log")), policy).unwrap();
        let addr = start(port, true, Some(log));
        let mut c = client::Client::connect(&addr).unwrap();
        let begin = Instant::now();
        for i in 0..2000 {
            c.request(&format!("SET k{} v", i % 1000)).unwrap();
        }
        println!("{name:>18} {:>9.1}", 2.0 / begin.elapsed().as_secs_f64());
    }
}
