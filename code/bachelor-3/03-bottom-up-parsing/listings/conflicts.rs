// conflicts.rs -- the SLR conflicts of each grammar file, and what LR(1)
// and LALR make of them.
// capture: args=ifelse.grammar lr.grammar expr.grammar
#[path = "../../02-top-down-parsing/listings/grammar.rs"]
mod grammar;
#[path = "lr0.rs"]
mod lr0;
#[path = "lr1.rs"]
mod lr1;
#[path = "slr.rs"]
mod slr;

fn main() {
    for file in std::env::args().skip(1) {
        let g = lr0::augment(&grammar::Grammar::parse(&std::fs::read_to_string(&file).expect("cannot read")));
        let a = lr0::automaton(&g);
        let t = slr::table(&g, &a);
        println!("== {file}: {} LR(0) states", a.states.len());
        for ((state, x), acts) in slr::conflicts(&t) {
            let shown: Vec<String> = acts.iter().map(|act| match act {
                slr::Action::Shift(j) => format!("shift {j}"),
                slr::Action::Reduce(r) => format!("reduce by {}", grammar::show_rule(&g, *r)),
                slr::Action::Accept => "accept".into(),
            }).collect();
            println!("  SLR conflict in state {state} on {x}: {}", shown.join(" / "));
        }
        let one = lr1::automaton1(&g);
        let la = lr1::lalr(&one);
        println!("  LR(1): {} states, conflicting cells {}; LALR: {} states, conflicting cells {}",
                 one.states.len(), lr1::conflicts1(&g, &one), la.states.len(), lr1::conflicts1(&g, &la));
    }
}
