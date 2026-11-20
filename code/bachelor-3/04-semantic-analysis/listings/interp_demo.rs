// interp_demo.rs -- check a program, then run it with the interpreter.
// capture: args=sieve.moor
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
#[path = "interp.rs"]
mod interp;

fn main() {
    let file = std::env::args().nth(1).expect("usage: interp_demo FILE");
    let src = std::fs::read_to_string(&file).expect("cannot read");
    let (prog, _, _) = typecheck::check_source(&src, &file).unwrap_or_else(|e| {
        eprint!("{e}");
        std::process::exit(1)
    });
    let run = interp::run(&prog, &[], 1_000_000);
    print!("{}", run.output);
    match run.exit {
        Ok(code) => println!("exit status {code} after {} statements", run.steps),
        Err(msg) => println!("runtime error: {msg}"),
    }
}
