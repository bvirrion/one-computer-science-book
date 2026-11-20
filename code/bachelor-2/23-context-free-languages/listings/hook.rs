// hook.rs: a two-rule grammar for balanced brackets, against a counter, up to length 10.
#[allow(dead_code)]
mod grammar;

fn balanced(w: &str) -> bool {
    let mut depth = 0i32;
    for c in w.chars() {
        depth += if c == '(' { 1 } else { -1 };
        if depth < 0 {
            return false; // a ) with no ( to close
        }
    }
    depth == 0
}

fn main() {
    let g = grammar::Grammar::parse("S -> ( S ) S | ε");
    println!("{}", g.show());
    let words = g.generated(10);
    let mut short: Vec<&String> = words.iter().filter(|w| w.len() <= 6).collect();
    short.sort_by_key(|w| w.len());
    println!("generated, up to length 6: {short:?}");
    for n in (0..=10).step_by(2) {
        let bracket = |m: u32, i: usize| if m >> i & 1 == 0 { '(' } else { ')' };
        let all = (0..1u32 << n).map(|m| (0..n).map(|i| bracket(m, i)).collect::<String>());
        let good: Vec<String> = all.filter(|w| balanced(w)).collect(); // all 2^n words tried
        let same = good.iter().all(|w| words.contains(w))
            && words.iter().filter(|w| w.len() == n).count() == good.len();
        let k = good.len();
        println!("length {n:2}: {k:3} balanced words; generated, and nothing else: {same}");
    }
}
