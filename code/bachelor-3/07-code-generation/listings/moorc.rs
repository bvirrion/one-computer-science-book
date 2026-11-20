// moorc.rs -- the Moor compiler: source file in, RISC-V assembly out.
// Usage: moorc FILE.moor > FILE.S
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
#[path = "frame.rs"]
mod frame;
#[path = "riscv.rs"]
mod riscv;

fn main() {
    let file = std::env::args().nth(1).expect("usage: moorc FILE.moor");
    let src = std::fs::read_to_string(&file).expect("a readable file");
    let result = typecheck::check_source(&src, &file)
        .and_then(|(prog, res, _)| riscv::program(&prog, &tac::translate(&prog, &res), None));
    match result {
        Ok(asm) => print!("{asm}"),
        Err(msg) => {
            eprint!("{msg}");
            std::process::exit(1);
        }
    }
}
