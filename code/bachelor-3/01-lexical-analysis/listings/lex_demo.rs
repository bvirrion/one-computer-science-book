// lex_demo.rs -- the token stream of a Moor file.
// capture: args=hello.moor
#[path = "token.rs"]
mod token;
#[path = "lexer.rs"]
mod lexer;

fn main() {
    let file = std::env::args().nth(1).expect("usage: lex_demo FILE");
    let src = std::fs::read_to_string(&file).expect("cannot read the file");
    match lexer::lex(&src) {
        Ok(tokens) => {
            for t in &tokens {
                let s = t.span;
                let lexeme = &src[s.start..s.end];
                let place = format!("{}:{}", s.line, s.col);
                println!("{:<6} {:<8} {}", place, token::class_name(&t.kind), lexeme);
            }
            println!("{} tokens", tokens.len());
        }
        Err(e) => print!("{}", lexer::show_error(&src, &file, &e)),
    }
}
