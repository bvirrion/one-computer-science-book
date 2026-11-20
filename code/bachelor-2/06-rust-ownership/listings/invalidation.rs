// capture: exit
// invalidation.rs: the loop of the previous chapter, in Rust.
fn main() {
    let mut due = vec![3, 8, 12, 20];
    for d in &due {
        println!("due in {d} days");
        if *d > 10 {
            due.push(d + 21);
        }
    }
}
