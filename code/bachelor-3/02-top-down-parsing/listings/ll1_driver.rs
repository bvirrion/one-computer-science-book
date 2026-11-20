// ll1_driver.rs -- the predictive parser as a pushdown automaton: the
// table decides, the stack remembers what is still expected.
// capture: args=expr.grammar
#[path = "grammar.rs"]
mod grammar;

fn main() {
    let file = std::env::args().nth(1).expect("usage: ll1_driver FILE");
    let g = grammar::Grammar::parse(&std::fs::read_to_string(file).expect("cannot read"));
    let t = grammar::table(&g, &grammar::compute(&g));
    let input: Vec<&str> = "id + id * id $".split(' ').collect();
    let mut stack = vec!["$".to_string(), g.start().to_string()]; // top at the end
    let mut i = 0;
    println!("{:<20} {:<16} action", "stack (top right)", "input");
    loop {
        let top = stack.last().unwrap().clone();
        let rest = input[i..].join(" ");
        print!("{:<20} {:<16} ", stack.join(" "), rest);
        if top == "$" && input[i] == "$" {
            println!("accept");
            return;
        }
        if !g.is_nt(&top) {
            if top != input[i] {
                println!("error: expected {top}");
                return;
            }
            println!("match {top}");
            stack.pop();
            i += 1;
            continue;
        }
        let Some(rules) = t.get(&(top.clone(), input[i].to_string())) else {
            println!("error: no rule for [{top}, {}]", input[i]);
            return;
        };
        let k = rules[0];
        println!("predict {}", grammar::show_rule(&g, k));
        stack.pop();
        stack.extend(g.rules[k].1.iter().rev().cloned());
    }
}
