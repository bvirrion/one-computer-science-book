// monitor_rust.rs -- the same monitor in Rust: the Mutex owns the state, so it cannot
// be touched without the lock, and Condvar::wait gives the lock back while asleep.
use std::collections::VecDeque;
use std::sync::{Arc, Condvar, Mutex};
use std::thread;

const CAP: usize = 8;

struct Buffer {
    items: Mutex<VecDeque<u64>>,
    not_full: Condvar,
    not_empty: Condvar,
}

impl Buffer {
    fn put(&self, x: u64) {
        let mut items = self.items.lock().unwrap();
        while items.len() == CAP {
            items = self.not_full.wait(items).unwrap(); // gives the lock back, retakes it
        }
        items.push_back(x);
        self.not_empty.notify_one();
    } // the guard is dropped here: unlocked

    fn take(&self) -> u64 {
        let mut items = self.items.lock().unwrap();
        while items.is_empty() {
            items = self.not_empty.wait(items).unwrap();
        }
        let x = items.pop_front().unwrap();
        self.not_full.notify_one();
        x
    }
}

fn main() {
    let (producers, consumers, per_producer) = (2u64, 2u64, 20_000u64);
    let buf = Arc::new(Buffer {
        items: Mutex::new(VecDeque::new()),
        not_full: Condvar::new(),
        not_empty: Condvar::new(),
    });
    let mut handles = Vec::new();
    for p in 0..producers {
        let b = Arc::clone(&buf);
        handles.push(thread::spawn(move || {
            (1..=per_producer).for_each(|i| b.put(p * per_producer + i));
            (0, 0) // a producer takes nothing
        }));
    }
    for _ in 0..consumers {
        let b = Arc::clone(&buf);
        let n = producers * per_producer / consumers;
        handles.push(thread::spawn(move || (n, (0..n).map(|_| b.take()).sum::<u64>())));
    }
    let (mut n, mut sum) = (0, 0);
    for h in handles {
        let (k, s) = h.join().unwrap();
        n += k;
        sum += s;
    }
    let total = producers * per_producer;
    println!("items taken: {n} of {total}");
    println!("sum taken:   {sum}, expected {}", total * (total + 1) / 2);
    println!("left in the buffer: {}", buf.items.lock().unwrap().len());
}
