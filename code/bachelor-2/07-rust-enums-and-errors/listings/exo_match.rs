// exo_match.rs: predict the five lines.
fn kind(n: i32) -> &'static str {
    match n {
        0 => "zero",
        x if x < 0 => "negative",
        1..=9 => "digit",
        10 | 100 | 1000 => "power of ten",
        _ => "other",
    }
}

fn main() {
    for n in [7, -3, 100, 0, 12] {
        let pair = (n % 2 == 0, n > 5);
        let size = match pair {
            (true, true) => "even and large",
            (true, false) => "even and small",
            (false, large) => if large { "odd and large" } else { "odd and small" },
        };
        println!("{n}: {}, {size}", kind(n));
    }
}
