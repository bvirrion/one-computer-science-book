// exo_runs.rs: five more words through the decimal-number automaton (exercise 1).
#[allow(dead_code)]
mod dfa_demo;

fn main() {
    for s in ["0.0", "-.5", "1E+10", "7e3.5", "+"] {
        let (ok, path) = dfa_demo::is_number(s);
        let verdict = if ok { "number" } else { "no" };
        println!("{:8} {verdict:6} states {path:?}", format!("{s:?}"));
    }
}
