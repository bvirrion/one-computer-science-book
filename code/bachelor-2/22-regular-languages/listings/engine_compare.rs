// engine_compare.rs: the Glushkov automaton on (a|a)*b and a^n: time and steps per letter.
#[allow(dead_code)]
mod regex;
use std::time::Instant;

fn main() {
    let g = regex::glushkov(&regex::parse("(a|a)*b").unwrap());
    let m = regex::Matcher::new(&g); // positions a1 a2 b3: m = 3
    println!("        n   matched      steps   steps/letter   time (ms)");
    for n in [20, 24, 1_000, 1_000_000, 10_000_000] {
        let text = "a".repeat(n);
        let t = Instant::now();
        let (matched, steps) = m.run(&text);
        let ms = t.elapsed().as_secs_f64() * 1e3;
        println!("{n:9} {matched:9} {steps:10} {:14.2} {ms:11.3}", steps as f64 / n as f64);
    }
}
