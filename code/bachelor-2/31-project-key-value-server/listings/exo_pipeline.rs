// capture: timeout=300
// exo_pipeline.rs (exercise 12): one client sends a batch of requests, then reads the replies.
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

use server::Shared;
use std::net::TcpListener;
use std::sync::Arc;
use std::thread;
use std::time::Instant;

fn main() -> std::io::Result<()> {
    let shared = Arc::new(Shared { store: Box::new(store::Sharded::new(16, store::Map::new())),
                                   log: None });
    let listener = TcpListener::bind("127.0.0.1:44319")?;
    thread::spawn(move || server::serve_pool(listener, shared, 4));
    let mut c = client::Client::connect("127.0.0.1:44319")?;
    c.request("SET k v")?;
    println!("batch   requests   k req/s   us per request");
    for batch in [1, 10, 100, 1000] {
        let total = 100_000;
        let start = Instant::now();
        for _ in 0..total / batch {
            c.write_raw("GET k\n".repeat(batch).as_bytes())?; // the whole batch in one write
            for _ in 0..batch {
                assert_eq!(c.receive()?, "VALUE v");
            }
        }
        let secs = start.elapsed().as_secs_f64();
        println!("{batch:>5} {total:>10} {:>9.1} {:>16.2}", total as f64 / secs / 1e3,
                 secs * 1e6 / total as f64);
    }
    Ok(())
}
