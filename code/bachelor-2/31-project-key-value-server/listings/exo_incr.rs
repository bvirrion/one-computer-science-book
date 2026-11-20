// exo_incr.rs (exercise 3): INCR as GET then SET loses an increment; under one lock, none.
use std::collections::HashMap;
use std::sync::{Arc, Barrier, Mutex};
use std::thread;

type Map = Arc<Mutex<HashMap<String, i64>>>;

/// GET, then SET of the value read plus one: two separate locked steps.
fn incr_get_then_set(map: &Map, key: &str, between: &Barrier) {
    let v = *map.lock().unwrap().get(key).unwrap_or(&0);
    between.wait(); // both clients have read before either writes
    map.lock().unwrap().insert(key.to_string(), v + 1);
}

/// INCR: read and write under one lock.
fn incr(map: &Map, key: &str) -> i64 {
    let mut m = map.lock().unwrap();
    let v = m.entry(key.to_string()).or_insert(0);
    *v += 1;
    *v
}

fn main() {
    let map: Map = Arc::new(Mutex::new(HashMap::new()));
    let between = Arc::new(Barrier::new(2));
    let clients: Vec<_> = (0..2).map(|_| {
        let (map, between) = (Arc::clone(&map), Arc::clone(&between));
        thread::spawn(move || incr_get_then_set(&map, "visits", &between))
    }).collect();
    clients.into_iter().for_each(|c| c.join().unwrap());
    println!("GET then SET, two clients: visits = {}", map.lock().unwrap()["visits"]);

    let map: Map = Arc::new(Mutex::new(HashMap::new()));
    let clients: Vec<_> = (0..8).map(|_| {
        let map = Arc::clone(&map);
        thread::spawn(move || (0..10_000).for_each(|_| { incr(&map, "visits"); }))
    }).collect();
    clients.into_iter().for_each(|c| c.join().unwrap());
    println!("INCR, 8 clients x 10000: visits = {}", map.lock().unwrap()["visits"]);
}
