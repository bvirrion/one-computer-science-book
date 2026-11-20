// scope_trace.rs -- the stack of scopes after each declaration.
// capture: args=ok.moor
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

fn main() {
    let file = std::env::args().nth(1).expect("usage: scope_trace FILE");
    let src = std::fs::read_to_string(&file).expect("cannot read");
    let prog = parser::parse_source(&src, &file).unwrap_or_else(|e| {
        eprint!("{e}");
        std::process::exit(1)
    });
    let r = resolve::resolve_traced(&prog, &mut |name, scopes| {
        let frames: Vec<String> = scopes.names().iter().map(|f| f.join(" ")).collect();
        println!("{name:<10} [{}]", frames.join("] ["));
    });
    println!("{} declarations, {} uses resolved", r.decls.len(), r.uses.len());
}
