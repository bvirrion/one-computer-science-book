// exo_leftmost.rs: a leftmost derivation of (a)*a (exercise 1).
#[allow(dead_code)]
mod grammar;

fn main() {
    let g = grammar::Grammar::parse("E -> E + T | T\nT -> T * F | F\nF -> ( E ) | a");
    for (i, form) in g.leftmost("(a)*a").unwrap().iter().enumerate() {
        println!("{} {}", if i == 0 { "  " } else { "=>" }, grammar::show(form));
    }
}
