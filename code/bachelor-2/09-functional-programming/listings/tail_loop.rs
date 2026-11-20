// tail_loop.rs: an accumulator holds the pending work; then a loop needs no stack.
fn sum_acc(xs: &[u64], acc: u64) -> u64 {
    match xs {
        [] => acc,
        [first, rest @ ..] => sum_acc(rest, acc + first), // a tail call: nothing waits for it
    }
}

fn sum_loop(mut xs: &[u64]) -> u64 {
    let mut acc = 0;
    while let [first, rest @ ..] = xs {
        // the same steps, with the call replaced by a jump
        acc += first;
        xs = rest;
    }
    acc
}

fn main() {
    let xs: Vec<u64> = (1..=1_000_000).collect();
    let small = std::thread::Builder::new().stack_size(1 << 20);
    let h = small.spawn(move || println!("{} {}", sum_loop(&xs), sum_acc(&xs[..1000], 0)));
    h.unwrap().join().unwrap();
}
