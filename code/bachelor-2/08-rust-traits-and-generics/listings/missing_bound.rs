// capture: exit
// missing_bound.rs: a generic function that compares values it knows nothing about.
fn largest<T: Copy>(xs: &[T]) -> T {
    let mut best = xs[0];
    for &x in xs {
        if x > best {
            best = x;
        }
    }
    best
}

fn main() {
    println!("{}", largest(&[65, 133, 98]));
}
