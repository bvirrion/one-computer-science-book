// exo_unit_cycle.rs: removing unit rules by following them recursively, on a grammar with
// a cycle of unit rules, then with a visited list (exercise 6).
#[allow(dead_code)]
mod grammar;
use grammar::{Grammar, Sym};

/// The naive way: the non-unit rules of `a`, then those reached through each unit rule.
fn naive(g: &Grammar, a: &str, depth: usize, path: &mut Vec<String>) -> Result<(), String> {
    path.push(a.to_string());
    if depth == 12 {
        return Err(path.join(" -> "));
    }
    for (b, rhs) in &g.rules {
        if let (true, [Sym::N(c)]) = (b == a, rhs.as_slice()) {
            naive(g, c, depth + 1, path)?;
        }
    }
    path.pop();
    Ok(())
}

fn main() {
    let g = Grammar::parse("S -> A | a b\nA -> B | a\nB -> A | b");
    println!("{}", g.show());
    match naive(&g, "S", 0, &mut vec![]) {
        Ok(()) => println!("naive: finished"),
        Err(path) => println!("naive: still going after 12 unit rules: {path} ..."),
    }
    let c = g.cnf();
    println!("with a list of the nonterminals already reached:\n{}", c.show());
}
