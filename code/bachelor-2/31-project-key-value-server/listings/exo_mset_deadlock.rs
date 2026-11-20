// exo_mset_deadlock.rs (exercise 6): two MSETs lock two shards in opposite orders, then not.
use std::sync::{Arc, Barrier, Mutex};
use std::thread;
use std::time::{Duration, Instant};

/// Wait at most 200 ms for a lock: a deadlock shows as a timeout instead of a hang.
fn lock_or_give_up(m: &Mutex<i32>) -> Option<std::sync::MutexGuard<'_, i32>> {
    let start = Instant::now();
    while start.elapsed() < Duration::from_millis(200) {
        if let Ok(g) = m.try_lock() {
            return Some(g);
        }
        thread::sleep(Duration::from_millis(1));
    }
    None
}

fn run(ordered: bool) {
    let shards = Arc::new([Mutex::new(0), Mutex::new(0)]);
    let (both_hold_one, both_tried) = (Arc::new(Barrier::new(2)), Arc::new(Barrier::new(2)));
    let mset = |name: &'static str, first: usize, second: usize| {
        let (shards, barrier) = (Arc::clone(&shards), Arc::clone(&both_hold_one));
        let tried = Arc::clone(&both_tried);
        thread::spawn(move || {
            let (a, b) = if ordered { (first.min(second), first.max(second)) }
                         else { (first, second) };
            let held = shards[a].lock().unwrap();
            if !ordered {
                barrier.wait(); // both have taken their first lock
            }
            let outcome = match lock_or_give_up(&shards[b]) {
                Some(_) => format!("  {name}: took shard {a}, then shard {b}: done"),
                None => format!("  {name}: holds shard {a}, waits for shard {b}: stuck"),
            };
            if !ordered {
                tried.wait(); // keep the first lock until both have given up
            }
            drop(held);
            outcome
        })
    };
    let (x, y) = (mset("MSET a b", 0, 1), mset("MSET b a", 1, 0));
    println!("{}\n{}", x.join().unwrap(), y.join().unwrap());
}

fn main() {
    println!("locks in the order of the keys:");
    run(false);
    println!("locks in increasing order of shard:");
    run(true);
}
