// parse_demo.rs -- parse a Moor file and print its abstract syntax tree.
// capture: args=fib.moor
#[path = "../../01-lexical-analysis/listings/token.rs"]
mod token;
#[path = "../../01-lexical-analysis/listings/lexer.rs"]
mod lexer;
#[path = "ast.rs"]
mod ast;
#[path = "parser.rs"]
mod parser;

fn main() {
    let file = std::env::args().nth(1).expect("usage: parse_demo FILE");
    let src = std::fs::read_to_string(&file).expect("cannot read the file");
    match parser::parse_source(&src, &file) {
        Ok(program) => print!("{}", ast::pretty(&program)),
        Err(messages) => print!("{messages}"),
    }
}
