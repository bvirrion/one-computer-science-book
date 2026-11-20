// tac_demo.rs -- the three-address code of every function of a program.
// capture: args=expr.moor
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

fn main() {
    let file = std::env::args().nth(1).expect("usage: tac_demo FILE.moor");
    let src = std::fs::read_to_string(&file).expect("a readable file");
    let (prog, res, _) = typecheck::check_source(&src, &file).unwrap_or_else(|m| panic!("{m}"));
    for f in tac::translate(&prog, &res) {
        println!("{}: {} temporaries", f.name, f.temps);
        for (k, ins) in f.code.iter().enumerate() {
            let indent = if matches!(ins, tac::Tac::Label(_)) { "" } else { "    " };
            println!("{k:>3}  {indent}{}", tac::show(&f, ins));
        }
    }
}
