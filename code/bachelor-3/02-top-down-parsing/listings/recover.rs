// recover.rs -- every syntax error of a file, thanks to panic mode.
// capture: args=errors.moor
#[path = "../../01-lexical-analysis/listings/token.rs"]
mod token;
#[path = "../../01-lexical-analysis/listings/lexer.rs"]
mod lexer;
#[path = "ast.rs"]
mod ast;
#[path = "parser.rs"]
mod parser;

fn main() {
    let file = std::env::args().nth(1).expect("usage: recover FILE");
    let src = std::fs::read_to_string(&file).expect("cannot read the file");
    let tokens = lexer::lex(&src).expect("no lexical error in this file");
    let mut p = parser::Parser::new(&tokens);
    let program = p.program();
    for e in &p.errors {
        print!("{}", parser::show(&src, &file, e));
    }
    println!("{} errors; the tree still has {} function(s)", p.errors.len(), program.items.len());
}
