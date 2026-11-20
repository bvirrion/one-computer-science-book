// lex_error.rs -- every lexical error of a file, each with a caret.
// capture: args=bad.moor
#[path = "token.rs"]
mod token;
#[path = "lexer.rs"]
mod lexer;

fn main() {
    let file = std::env::args().nth(1).expect("usage: lex_error FILE");
    let src = std::fs::read_to_string(&file).expect("cannot read the file");
    let (tokens, errors) = lexer::lex_recover(&src);
    for e in &errors {
        print!("{}", lexer::show_error(&src, &file, e));
    }
    println!("{} errors, {} tokens kept", errors.len(), tokens.len());
}
