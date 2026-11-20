// sr_trace.rs -- the shift-reduce parser on id + id * id.
// capture: args=expr.grammar
#[path = "../../02-top-down-parsing/listings/grammar.rs"]
mod grammar;
#[path = "lr0.rs"]
mod lr0;
#[path = "slr.rs"]
mod slr;

fn main() {
    let file = std::env::args().nth(1).expect("usage: sr_trace FILE");
    let g = lr0::augment(&grammar::Grammar::parse(&std::fs::read_to_string(file).expect("cannot read")));
    let t = slr::table(&g, &lr0::automaton(&g));
    println!("{:<5} {:<14} {:<16} action", "state", "symbols", "input");
    let input = ["id", "+", "id", "*", "id", "$"];
    let reduced = slr::parse(&g, &t, &input, true).unwrap();
    let rules: Vec<String> = reduced.iter().map(|r| r.to_string()).collect();
    println!("rules reduced: {}", rules.join(" "));
}
