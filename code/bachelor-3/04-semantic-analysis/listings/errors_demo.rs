// errors_demo.rs -- the front end on a program with mistakes.
// capture: args=errors.moor
#[path = "../../01-lexical-analysis/listings/token.rs"]
mod token;
#[path = "../../01-lexical-analysis/listings/lexer.rs"]
mod lexer;
#[path = "../../02-top-down-parsing/listings/ast.rs"]
mod ast;
#[path = "../../02-top-down-parsing/listings/parser.rs"]
mod parser;
#[path = "scope.rs"]
mod scope;
#[path = "resolve.rs"]
mod resolve;
#[path = "typecheck.rs"]
mod typecheck;

fn main() {
    let file = std::env::args().nth(1).expect("usage: errors_demo FILE");
    let src = std::fs::read_to_string(&file).expect("cannot read");
    match typecheck::check_source(&src, &file) {
        Ok(_) => println!("no error"),
        Err(e) => print!("{e}"),
    }
}
