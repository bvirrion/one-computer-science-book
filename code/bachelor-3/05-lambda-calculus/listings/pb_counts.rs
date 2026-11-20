// pb_counts.rs -- beta-steps of Church arithmetic under normal order and
// applicative order, for the weekend problem.
#![allow(dead_code)]
#[path = "term.rs"]
mod term;
#[path = "reduce.rs"]
mod reduce;
#[path = "encode.rs"]
mod encode;
use reduce::Strategy::{self, Applicative, Normal};

/// Steps to normal form of `op` applied to the numerals m and n.
fn steps(op: &str, m: usize, n: Option<usize>, s: Strategy) -> usize {
    let mut t = term::app(encode::church(op), encode::numeral(m));
    if let Some(n) = n {
        t = term::app(t, encode::numeral(n));
    }
    let (nf, k, done) = reduce::run(&t, s, 1_000_000);
    assert!(done && encode::value(&nf).is_some(), "{op} {m} {n:?}");
    k
}

fn main() {
    let sub = r"\m n. n pred m";
    println!(" n  mult n 3  exp 2 n   pred n      sub 10 n");
    println!("    nor app   nor app   nor app    nor   app");
    for n in 0..=10 {
        let e = if (1..=5).contains(&n) { format!("{:>3} {:>3}", steps("exp", 2, Some(n), Normal),
                                    steps("exp", 2, Some(n), Applicative)) } else { "  -   -".into() };
        println!("{n:>2}  {:>3} {:>3}   {e}   {:>3} {:>3}   {:>4} {:>5}",
                 steps("mult", n, Some(3), Normal), steps("mult", n, Some(3), Applicative),
                 steps("pred", n, None, Normal), steps("pred", n, None, Applicative),
                 steps(sub, 10, Some(n), Normal), steps(sub, 10, Some(n), Applicative));
    }
}
