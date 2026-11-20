// arc_mutex.rs: four threads share one counter through Arc<Mutex<_>>.
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let count = Arc::new(Mutex::new(0_u64));     // shared ownership of a locked value
    let mut handles = Vec::new();
    for _ in 0..4 {
        let count = Arc::clone(&count);          // one owner more per thread
        handles.push(thread::spawn(move || {
            for _ in 0..1_000_000 {
                *count.lock().unwrap() += 1;     // the guard unlocks at the end of the line
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }
    println!("count = {}", *count.lock().unwrap());
}
