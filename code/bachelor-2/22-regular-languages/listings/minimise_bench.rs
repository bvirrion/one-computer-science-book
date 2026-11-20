// minimise_bench.rs: Moore against Hopcroft on large automata (exercise 11).
#[allow(dead_code)]
mod dfa;
#[allow(dead_code)]
mod regex;
#[path = "../exercises/hopcroft.rs"]
mod hopcroft;
use std::time::Instant;

fn main() {
    println!(" k   DFA states  minimal  Moore rounds  Moore (ms)  Hopcroft (ms)");
    for k in [8, 10, 12, 14] {
        // a redundant automaton: "the k-th letter from the end is a", or a word of b's
        let text = format!("(a|b)*a(a|b){{{k}}}|(a|b)*a(a|b){{{k}}}b*|b*");
        let g = regex::glushkov(&regex::parse(&text).unwrap());
        let d = dfa::determinise(&g, &['a', 'b']);
        let t = Instant::now();
        let rounds = dfa::moore(&d);
        let moore_ms = t.elapsed().as_secs_f64() * 1e3;
        let t = Instant::now();
        let classes = hopcroft::hopcroft(&d);
        let hopcroft_ms = t.elapsed().as_secs_f64() * 1e3;
        assert_eq!(&classes, rounds.last().unwrap()); // the same partition
        let minimal = classes.iter().max().unwrap() + 1;
        println!("{k:2} {:12} {minimal:8} {:13} {moore_ms:11.1} {hopcroft_ms:14.1}",
                 d.delta.len(), rounds.len());
    }
}
