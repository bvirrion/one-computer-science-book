// church.rs -- numbers, booleans and pairs as functions, and how many
// beta-steps two strategies take to compute with them.
#![allow(dead_code)]
#[path = "term.rs"]
mod term;
#[path = "reduce.rs"]
mod reduce;
#[path = "encode.rs"]
mod encode;
use reduce::Strategy;

fn main() {
    println!("{:<16} {:>6} {:>12}   normal form", "term", "normal", "applicative");
    for src in ["succ c2", "plus c2 c3", "mult c2 c3", "exp c2 c3", "pred c3", "fst (pair c1 c2)"] {
        let t = encode::church(src);
        let (nf, n1, _) = reduce::run(&t, Strategy::Normal, 10_000);
        let (_, n2, _) = reduce::run(&t, Strategy::Applicative, 10_000);
        let shown = encode::value(&nf).map_or(term::show(&nf), |v| format!("{}  (the numeral {v})", term::show(&nf)));
        println!("{src:<16} {n1:>6} {n2:>12}   {shown}");
    }
}
