// live_demo.rs -- the temporaries live at the start and the end of each
// block of a function, and the worklist's visits.
// capture: args=loop.moor
#![allow(dead_code)]
#[path = "../../01-lexical-analysis/listings/token.rs"]
mod token;
#[path = "../../01-lexical-analysis/listings/lexer.rs"]
mod lexer;
#[path = "../../02-top-down-parsing/listings/ast.rs"]
mod ast;
#[path = "../../02-top-down-parsing/listings/parser.rs"]
mod parser;
#[path = "../../04-semantic-analysis/listings/scope.rs"]
mod scope;
#[path = "../../04-semantic-analysis/listings/resolve.rs"]
mod resolve;
#[path = "../../04-semantic-analysis/listings/typecheck.rs"]
mod typecheck;
#[path = "../../07-code-generation/listings/tac.rs"]
mod tac;
#[path = "../../07-code-generation/listings/cfg.rs"]
mod cfg;
#[path = "dataflow.rs"]
mod dataflow;
#[path = "liveness.rs"]
mod liveness;

fn names(f: &tac::FuncTac, s: &liveness::Set) -> String {
    let v: Vec<String> = s.iter().map(|&t| tac::val(f, tac::Val::T(t))).collect();
    format!("{{{}}}", v.join(", "))
}

fn main() {
    let file = std::env::args().nth(1).expect("usage: live_demo FILE.moor");
    let src = std::fs::read_to_string(&file).expect("a readable file");
    let (prog, res, _) = typecheck::check_source(&src, &file).unwrap_or_else(|m| panic!("{m}"));
    let funcs = tac::translate(&prog, &res);
    let f = &funcs[0];
    let g = cfg::build(f);
    let sol = dataflow::solve(&liveness::Liveness { code: &f.code, g: &g }, &g);
    for (b, &(s, e)) in g.blocks.iter().enumerate() {
        println!("B{b}  live in {}", names(f, &sol.before[b]));
        for i in &f.code[s..e] {
            println!("        {}", tac::show(f, i));
        }
        println!("    live out {}", names(f, &sol.after[b]));
    }
    println!("{} blocks, {} visits", g.blocks.len(), sol.visits);
}
