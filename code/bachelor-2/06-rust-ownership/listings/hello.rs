// hello.rs: Rust in one screen: bindings, mutability, types, functions, a loop, a vector.
fn fine_cents(days_late: u32) -> u32 {
    // the last expression, with no semicolon, is the value returned
    (10 * days_late).min(500)
}

fn main() {
    let town = "Riverside"; // immutable by default; its type, &str, is inferred
    let mut total: u32 = 0; // mut: this binding may change
    let delays = vec![3, 0, 12, 75]; // a Vec<u32>, growable, on the heap
    for d in &delays {
        total += fine_cents(*d);
    }
    let average = total as f64 / delays.len() as f64; // no implicit conversions: `as`
    println!("{town}: {} loans, {total} cents of fines, {average:.2} on average",
        delays.len());
    let big: u8 = 250;
    println!("{:?} {:?} {}", big.checked_add(10), big.checked_add(5), big.wrapping_add(10));
}
