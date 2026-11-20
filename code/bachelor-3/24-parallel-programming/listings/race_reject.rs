// race_reject.rs -- two scoped threads add to one counter through the same variable.
// The borrow checker refuses the program: a data race cannot be compiled.
// capture: exit
use std::thread;

fn main() {
    let mut count = 0u64;
    thread::scope(|s| {
        s.spawn(|| {
            for _ in 0..1000 {
                count += 1;
            }
        });
        s.spawn(|| {
            for _ in 0..1000 {
                count += 1;
            }
        });
    });
    println!("{count}");
}
