// odd_squares.rs: the sum of the squares of the odd readings, as a loop and as one expression.
fn main() {
    let readings = [12, 7, 3, 20, 9, 4, 15];

    let mut total = 0;
    for r in readings {
        if r % 2 == 1 {
            total += r * r;
        }
    }

    let total2: i32 = readings.iter().filter(|&&r| r % 2 == 1).map(|r| r * r).sum();
    println!("{total} {total2}");
}
