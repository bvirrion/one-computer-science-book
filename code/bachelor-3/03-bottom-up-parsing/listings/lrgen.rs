// lrgen.rs -- the generator as a command: grammar file in, Rust tables out.
// capture: args=moor_expr.grammar
#[path = "../../02-top-down-parsing/listings/grammar.rs"]
mod grammar;
#[path = "lr0.rs"]
mod lr0;
#[path = "slr.rs"]
mod slr;
#[path = "gen.rs"]
mod gen;

fn main() {
    let file = std::env::args().nth(1).expect("usage: lrgen FILE");
    let g = grammar::Grammar::parse(&std::fs::read_to_string(&file).expect("cannot read"));
    match gen::emit(&file, &g) {
        Ok(src) => print!("{src}"),
        Err(e) => {
            eprintln!("lrgen: {file}: {e}");
            std::process::exit(1);
        }
    }
}
