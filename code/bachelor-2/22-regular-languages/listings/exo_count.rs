// exo_count.rs: the words of each length in (ab|b)*, from the denotation (exercise 4).
#[allow(dead_code)]
mod regex;

fn main() {
    let words = regex::lang(&regex::parse("(ab|b)*").unwrap(), 12);
    let counts: Vec<usize> = (0..=12).map(|n| words.iter().filter(|w| w.len() == n).count())
        .collect();
    println!("{counts:?}");
}
