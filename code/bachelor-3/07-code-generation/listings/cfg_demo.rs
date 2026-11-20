// cfg_demo.rs -- the basic blocks of each function, and the edges
// between them.
// capture: args=fib.moor
#![allow(dead_code)]
#[path = "../../01-lexical-analysis/listings/token.rs"]
mod token;
#[path = "../../01-lexical-analysis/listings/lexer.rs"]
mod lexer;
#[path = "../../02-top-down-parsing/listings/ast.rs"]
mod ast;
#[path = "../../02-top-down-parsing/listings/parser.rs"]
mod parser;
#[path = "../../04-semantic-analysis/listings/scope.rs"]
mod scope;
#[path = "../../04-semantic-analysis/listings/resolve.rs"]
mod resolve;
#[path = "../../04-semantic-analysis/listings/typecheck.rs"]
mod typecheck;
#[path = "tac.rs"]
mod tac;
#[path = "cfg.rs"]
mod cfg;

fn main() {
    let file = std::env::args().nth(1).expect("usage: cfg_demo FILE.moor");
    let src = std::fs::read_to_string(&file).expect("a readable file");
    let (prog, res, _) = typecheck::check_source(&src, &file).unwrap_or_else(|m| panic!("{m}"));
    for f in tac::translate(&prog, &res).iter().filter(|f| f.name == "fib") {
        let g = cfg::build(f);
        for (k, &(s, e)) in g.blocks.iter().enumerate() {
            let to: Vec<String> = g.succ[k].iter().map(|b| format!("B{b}")).collect();
            let to = if to.is_empty() { "exit".to_string() } else { to.join(", ") };
            println!("B{k}  (instructions {s}..{})  -> {to}", e - 1);
            for ins in &f.code[s..e] {
                println!("        {}", tac::show(f, ins));
            }
        }
    }
}
