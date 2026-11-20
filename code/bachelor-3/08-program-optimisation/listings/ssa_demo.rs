// ssa_demo.rs -- the dominators, frontiers and SSA form of a function.
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
#[path = "ssa.rs"]
mod ssa;

fn set(s: &std::collections::BTreeSet<usize>) -> String {
    let v: Vec<String> = s.iter().map(|b| format!("B{b}")).collect();
    format!("{{{}}}", v.join(", "))
}

fn main() {
    let file = std::env::args().nth(1).expect("usage: ssa_demo FILE.moor");
    let src = std::fs::read_to_string(&file).expect("a readable file");
    let (prog, res, _) = typecheck::check_source(&src, &file).unwrap_or_else(|m| panic!("{m}"));
    let funcs = tac::translate(&prog, &res);
    let f = &funcs[0];
    let g = cfg::build(f);
    let dom = ssa::dominators(&g);
    let id = ssa::idom(&dom);
    let df = ssa::frontiers(&g, &id);
    let live = ssa::reachable(&g);
    for b in (0..g.blocks.len()).filter(|&b| live[b]) {
        let i = id[b].map_or("-".to_string(), |d| format!("B{d}"));
        println!("B{b}  dom {}  idom {i}  frontier {}", set(&dom[b]), set(&df[b]));
    }
    let s = ssa::to_ssa(f, &g);
    println!("SSA form, {} phi-functions:", s.count);
    for b in (0..g.blocks.len()).filter(|&b| live[b]) {
        println!("B{b}");
        let label = s.code[b].first().filter(|l| l.ends_with(':')); // phis go after the label
        let rest = &s.code[b][label.is_some() as usize..];
        for line in label.into_iter().chain(&s.phis[b]).chain(rest) {
            println!("    {line}");
        }
    }
}
