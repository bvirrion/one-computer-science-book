// lazy.rs: iterator adaptors do nothing until something consumes them.
fn main() {
    let pages = [65, 133, 412, 98, 251, 320];
    let it = pages
        .iter()
        .map(|p| {
            println!("  map {p}");
            p * 2
        })
        .filter(|d| {
            println!("  filter {d}");
            *d > 300
        });
    println!("nothing has run yet");
    let first_two: Vec<i32> = it.take(2).collect(); // the consumer pulls, one at a time
    println!("{first_two:?}");
}
