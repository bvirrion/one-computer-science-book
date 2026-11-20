// slr_table.rs -- the SLR action and goto table, one row per state.
// capture: args=expr.grammar
#[path = "../../02-top-down-parsing/listings/grammar.rs"]
mod grammar;
#[path = "lr0.rs"]
mod lr0;
#[path = "slr.rs"]
mod slr;
use slr::Action;

fn main() {
    let file = std::env::args().nth(1).expect("usage: slr_table FILE");
    let g = lr0::augment(&grammar::Grammar::parse(&std::fs::read_to_string(file).expect("cannot read")));
    let t = slr::table(&g, &lr0::automaton(&g));
    let terms = ["id", "+", "*", "(", ")", "$"];
    let nts = ["E", "T", "F"];
    println!("state {}  | {}", terms.map(|x| format!("{x:<4}")).join(""), nts.map(|x| format!("{x:<3}")).join(""));
    for k in 0..12 {
        let cell = |x: &str| match t.action.get(&(k, x.to_string())).map(|v| v[0]) {
            Some(Action::Shift(j)) => format!("s{j}"),
            Some(Action::Reduce(r)) => format!("r{r}"),
            Some(Action::Accept) => "acc".into(),
            None => String::new(),
        };
        let go = |x: &str| t.goto.get(&(k, x.to_string())).map_or(String::new(), |j| j.to_string());
        println!("{k:>5} {}  | {}", terms.map(|x| format!("{:<4}", cell(x))).join(""),
                 nts.map(|x| format!("{:<3}", go(x))).join(""));
    }
    println!("conflicts: {}", slr::conflicts(&t).len());
}
