// first_follow.rs -- nullable, FIRST and FOLLOW of a grammar file.
// capture: args=expr.grammar
#[path = "grammar.rs"]
mod grammar;

fn show(set: &grammar::Set) -> String {
    format!("{{{}}}", set.iter().cloned().collect::<Vec<_>>().join(", "))
}

fn main() {
    let file = std::env::args().nth(1).expect("usage: first_follow FILE");
    let g = grammar::Grammar::parse(&std::fs::read_to_string(file).expect("cannot read"));
    let s = grammar::compute(&g);
    println!("{:<4} {:<9} {:<16} FOLLOW", "", "nullable", "FIRST");
    for a in &g.nonterms {
        let null = if s.nullable.contains(a) { "yes" } else { "no" };
        println!("{:<4} {:<9} {:<16} {}", a, null, show(&s.first[a]), show(&s.follow[a]));
    }
    println!("passes until stable: FIRST {}, FOLLOW {}", s.rounds.0, s.rounds.1);
}
