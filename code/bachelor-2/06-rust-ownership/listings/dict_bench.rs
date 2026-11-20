// dict_bench.rs: the same 4 million words, counted with dict_table.rs.
#[allow(dead_code)] // the benchmark uses only part of the table
mod dict_table;
use dict_table::Dict;
use std::fmt::Write;
use std::time::Instant;

fn main() {
    let t0 = Instant::now();
    let mut d = Dict::default();
    let mut x: u64 = 2025;
    let mut word = String::with_capacity(16); // one buffer, reused as in C
    for _ in 0..4_000_000 {
        x = x.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        word.clear();
        write!(word, "w{}", (x >> 33) % 100000).unwrap();
        *d.count(&word) += 1;
    }
    let w7 = *d.count("w7");
    let len = d.len();
    drop(d);
    println!("Rust: {len} different, w7 {w7} times, {:.0} ms", t0.elapsed().as_secs_f64() * 1e3);
}
