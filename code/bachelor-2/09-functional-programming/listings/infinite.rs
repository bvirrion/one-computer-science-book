// infinite.rs: infinite iterators are fine, as long as the consumer stops.
fn main() {
    let squares: Vec<u64> = (1..).map(|n| n * n).take_while(|&s| s < 100).collect();
    println!("{squares:?}");

    // the Fibonacci numbers, each pair made from the previous one
    let pairs = std::iter::successors(Some((0u64, 1u64)), |&(a, b)| Some((b, a + b)));
    let fib = pairs.map(|(a, _)| a);
    println!("{:?}", fib.clone().take(12).collect::<Vec<_>>());
    println!("first above a million: {:?}", fib.clone().find(|&f| f > 1_000_000));

    // the stopping times of a 3n + 1 walk: generated until it reaches 1
    let walk = std::iter::successors(Some(27u64), |&n| {
        if n == 1 { None } else if n % 2 == 0 { Some(n / 2) } else { Some(3 * n + 1) }
    });
    let steps = walk.clone().count() - 1;
    println!("27 reaches 1 after {steps} steps, peaking at {}", walk.max().unwrap());
}
