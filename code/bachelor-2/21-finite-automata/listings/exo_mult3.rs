// exo_mult3.rs: the DFA of the binary multiples of 3 (exercise 3).
#[allow(dead_code)]
#[path = "../exercises/multiples.rs"]
mod multiples;

fn main() {
    for (r, row) in multiples::delta(3, 2).iter().enumerate() {
        let mark = if r == 0 { "  (start, accepting)" } else { "" };
        println!("state {r}: 0 -> {}, 1 -> {}{mark}", row[0], row[1]);
    }
    let ok = (0..1000u32).all(|x| {
        let bits: Vec<u32> = format!("{x:b}").chars()
            .map(|c| c.to_digit(2).unwrap()).collect();
        multiples::is_multiple(3, 2, &bits) == (x % 3 == 0)
    });
    println!("agrees with x % 3 == 0 for x = 0 .. 999: {ok}");
}
