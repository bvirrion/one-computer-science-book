// kernel_bug.rs -- an LR(0) automaton whose goto forgets something.
// capture: args=expr.grammar
#[path = "../../02-top-down-parsing/listings/grammar.rs"]
mod grammar;
#[path = "lr0.rs"]
mod lr0;
#[path = "slr.rs"]
mod slr;
use lr0::{next_sym, Lr0, State};

fn goto(g: &grammar::Grammar, items: &State, x: &str) -> State {
    items.iter().filter(|&&it| next_sym(g, it).map(|s| s.as_str()) == Some(x))
        .map(|&(r, d)| (r, d + 1)).collect()
}

fn automaton(g: &grammar::Grammar) -> Lr0 {
    let mut a = Lr0 { states: vec![lr0::closure(g, &State::from([(0, 0)]))], trans: Default::default() };
    let mut k = 0;
    while k < a.states.len() {
        let syms: Vec<String> = a.states[k].iter().filter_map(|&it| next_sym(g, it).cloned()).collect();
        for x in syms {
            let target = goto(g, &a.states[k], &x);
            let j = a.states.iter().position(|s| *s == target).unwrap_or_else(|| {
                a.states.push(target);
                a.states.len() - 1
            });
            a.trans.insert((k, x), j);
        }
        k += 1;
    }
    a
}

fn main() {
    let file = std::env::args().nth(1).expect("usage: kernel_bug FILE");
    let g = lr0::augment(&grammar::Grammar::parse(&std::fs::read_to_string(file).expect("cannot read")));
    let a = automaton(&g);
    let t = slr::table(&g, &a);
    println!("{} states", a.states.len());
    for input in [vec!["id", "$"], vec!["id", "+", "id", "$"], vec!["id", "*", "id", "$"]] {
        let result = slr::parse(&g, &t, &input, false);
        println!("{:<14} {:?}", input.join(" "), result);
    }
}
