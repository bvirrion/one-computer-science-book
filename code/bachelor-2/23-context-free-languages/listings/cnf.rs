// cnf.rs: the expression grammar with levels, in Chomsky normal form.
#[allow(dead_code)]
mod grammar;

fn main() {
    let g = grammar::Grammar::parse("E -> E + T | T\nT -> T * F | F\nF -> ( E ) | a");
    let c = g.cnf();
    println!("{}", c.show());
    let size = |g: &grammar::Grammar| -> usize {
        g.rules.iter().map(|(_, rhs)| 1 + rhs.len()).sum() // a rule A -> X Y counts 3
    };
    let (r, s) = ((g.rules.len(), c.rules.len()), (size(&g), size(&c)));
    println!("rules: {} -> {}; size: {} -> {}", r.0, r.1, s.0, s.1);
    let all = g.generated(9);
    let same = all.iter().all(|w| c.accepts(w)) && c.generated(9) == all;
    println!("the same {} words up to length 9: {same}", all.len());
}
