// dict.rs: dict.c in Rust: count the words of standard input.
mod dict_table;
use dict_table::Dict;
use std::io::BufRead;

fn main() {
    let mut d = Dict::default();
    for line in std::io::stdin().lock().lines() {
        let line = line.expect("unreadable input"); // a fresh String each line, dropped at the end of the body
        for w in line.split([' ', ',']).filter(|w| !w.is_empty()) {
            *d.count(w) += 1;
        }
    }
    if d.is_empty() {
        return println!("no words");
    }
    let (best, most) = d.iter().max_by_key(|&(_, c)| c).unwrap();
    println!("{} different words; most frequent: {best} ({most})", d.len());
} // d is dropped here: every word, then the slots
