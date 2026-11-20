// lr0_states.rs -- the LR(0) automaton of a grammar: each state's items
// and where each symbol leads.
// capture: args=expr.grammar
#[path = "../../02-top-down-parsing/listings/grammar.rs"]
mod grammar;
#[path = "lr0.rs"]
mod lr0;

fn main() {
    let file = std::env::args().nth(1).expect("usage: lr0_states FILE");
    let g = lr0::augment(&grammar::Grammar::parse(&std::fs::read_to_string(file).expect("cannot read")));
    let a = lr0::automaton(&g);
    for (k, state) in a.states.iter().enumerate() {
        // kernel items (dot not at the start, or the start rule) first
        let mut its: Vec<_> = state.iter().copied().collect();
        its.sort_by_key(|&(r, d)| (d == 0 && r != 0, r));
        let items: Vec<String> = its.iter().map(|&it| lr0::show_item(&g, it)).collect();
        let moves: Vec<String> = a.trans.iter().filter(|((from, _), _)| *from == k)
            .map(|((_, x), to)| format!("{x}:{to}")).collect();
        println!("I{k:<2} {:<22} {}", items[0], moves.join(" "));
        for it in &items[1..] {
            println!("    {it}");
        }
    }
    println!("{} states", a.states.len());
}
