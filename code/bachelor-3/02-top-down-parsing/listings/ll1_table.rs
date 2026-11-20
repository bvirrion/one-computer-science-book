// ll1_table.rs -- the LL(1) table of each grammar file, and its conflicts.
// capture: args=stmt.grammar stmt_factored.grammar
#[path = "grammar.rs"]
mod grammar;

fn main() {
    for file in std::env::args().skip(1) {
        let g = grammar::Grammar::parse(&std::fs::read_to_string(&file).expect("cannot read"));
        let t = grammar::table(&g, &grammar::compute(&g));
        println!("== {file}");
        let mut conflicts = 0;
        for ((a, x), rules) in &t {
            let shown: Vec<String> = rules.iter().map(|&k| grammar::show_rule(&g, k)).collect();
            let mark = if rules.len() > 1 { "  <-- conflict" } else { "" };
            println!("  [{a}, {x}] {}{mark}", shown.join("  /  "));
            conflicts += usize::from(rules.len() > 1);
        }
        println!("  {} cells, {} with a conflict: {}", t.len(), conflicts,
                 if conflicts == 0 { "LL(1)" } else { "not LL(1)" });
    }
}
