// prec_demo.rs -- what precedence climbing builds for a few expressions.
#[path = "../../01-lexical-analysis/listings/token.rs"]
mod token;
#[path = "../../01-lexical-analysis/listings/lexer.rs"]
mod lexer;
#[path = "ast.rs"]
mod ast;
#[path = "parser.rs"]
mod parser;

fn main() {
    for src in ["1 - 2 - 3 * 4", "a + b * c", "-x * y", "!p && q || r", "a < b == c < d", "f(x, y + 1)[2]"] {
        match parser::parse_expr(src) {
            Ok(e) => println!("{src:<16} => {e}"),
            Err(msg) => println!("{src:<16} => error: {msg}"),
        }
    }
}
