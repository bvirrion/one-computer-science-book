// derive.rs: a leftmost derivation of a+a*a in the expression grammar with levels.
#[allow(dead_code)]
mod grammar;

fn main() {
    let g = grammar::Grammar::parse("E -> E + T | T\nT -> T * F | F\nF -> ( E ) | a");
    println!("{}", g.show());
    let steps = g.leftmost("a+a*a").unwrap();
    for (i, form) in steps.iter().enumerate() {
        println!("{} {}", if i == 0 { "  " } else { "=>" }, grammar::show(form));
    }
    let n = steps.len() - 1;
    println!("{n} steps, one per node of the parse tree that is not a letter");
}
