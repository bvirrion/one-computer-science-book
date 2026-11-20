// check_demo.rs -- every use of a name in a program, and its declaration.
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
#[path = "typecheck.rs"]
mod typecheck;
use resolve::Kind;

fn main() {
    let file = std::env::args().nth(1).expect("usage: check_demo FILE");
    let src = std::fs::read_to_string(&file).expect("cannot read");
    let (prog, r, tys) = typecheck::check_source(&src, &file).unwrap_or_else(|e| {
        eprint!("{e}");
        std::process::exit(1)
    });
    let mut uses: Vec<(&usize, &usize)> = r.uses.iter().collect();
    uses.sort();
    for (&at, &id) in uses {
        let d = &r.decls[id];
        let line = src[..at].matches('\n').count() + 1;
        let col = at - src[..at].rfind('\n').map_or(0, |k| k + 1) + 1;
        let place = match d.kind {
            Kind::Builtin => "built in".to_string(),
            _ => format!("{:?} at {}:{}", d.kind, d.span.line, d.span.col).to_lowercase(),
        };
        let ty = tys.get(&id).map_or(String::new(), |t| format!(": {}", t.name()));
        println!("{line:>2}:{col:<3} {:<6} -> {place}{ty}", d.name);
    }
    println!("{} items, {} declarations, {} uses: no error", prog.items.len(), r.decls.len(), r.uses.len());
}
