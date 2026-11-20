// exo_mset.rs (exercise 10): an atomic MSET across shards under load.
#[allow(dead_code)]
mod log;
#[allow(dead_code)]
#[path = "../exercises/mset.rs"]
mod mset;
#[allow(dead_code)]
mod protocol;
#[allow(dead_code)]
mod store;

use std::sync::Arc;
use std::thread;
use store::{shard_of, Map, Sharded};

fn main() {
    let store = Arc::new(Sharded::new(16, Map::new()));
    let keys = ["from", "to"]; // a transfer: both change together or neither
    println!("shards of the keys: {} and {}", shard_of("from", 16), shard_of("to", 16));
    mset::mset(&store, &[("from", "0"), ("to", "0")]);
    let writers: Vec<_> = (0..4).map(|t| {
        let s = Arc::clone(&store);
        thread::spawn(move || for i in 0..20_000 {
            let v = format!("{t}:{i}");
            let mut pairs = [("from", &*v), ("to", &*v)];
            if t % 2 == 1 {
                pairs.reverse(); // half the writers name the keys the other way round
            }
            mset::mset(&s, &pairs);
        })
    }).collect();
    let readers: Vec<_> = (0..4).map(|_| {
        let s = Arc::clone(&store);
        thread::spawn(move || (0..20_000).filter(|_| {
            let got = mset::mget(&s, &keys);
            got[0] != got[1]
        }).count())
    }).collect();
    writers.into_iter().for_each(|w| w.join().unwrap());
    let torn: usize = readers.into_iter().map(|r| r.join().unwrap()).sum();
    println!("4 writers x 20000 MSET, 4 readers x 20000 MGET: {torn} reads saw two values");
}
