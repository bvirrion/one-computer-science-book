// capture: exit
// deep_recursion.rs: a recursion one call per element; on a small stack it does not finish.
fn sum_rec(xs: &[u64]) -> u64 {
    match xs {
        [] => 0,
        [first, rest @ ..] => first + sum_rec(rest), // + waits: not a tail call
    }
}

fn main() {
    let xs: Vec<u64> = (1..=1_000_000).collect();
    let small = std::thread::Builder::new().stack_size(1 << 20); // a 1 MiB stack
    let h = small.spawn(move || println!("sum {}", sum_rec(&xs))).unwrap();
    h.join().unwrap();
}
