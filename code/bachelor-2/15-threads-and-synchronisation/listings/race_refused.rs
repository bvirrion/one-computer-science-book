// capture: exit
// race_refused.rs: a thread that borrows a local counter is refused.
use std::thread;

fn main() {
    let mut count = 0;
    let t = thread::spawn(|| {
        for _ in 0..1000 {
            count += 1;
        }
    });
    t.join().unwrap();
    println!("{count}");
}
