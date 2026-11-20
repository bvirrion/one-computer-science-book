// color_demo.rs -- the interference graph of the optimised function, then
// a colouring with k registers for each k given (3 and 4 by default).
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
#[path = "opt.rs"]
mod opt;
#[path = "regalloc.rs"]
mod regalloc;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let file = args.first().expect("usage: color_demo FILE.moor [K...]");
    let ks: Vec<usize> = args[1..].iter().map(|k| k.parse().unwrap()).collect();
    let ks = if ks.is_empty() { vec![3, 4] } else { ks };
    let src = std::fs::read_to_string(&file).expect("a readable file");
    let (prog, res, _) = typecheck::check_source(&src, file).unwrap_or_else(|m| panic!("{m}"));
    let mut f = tac::translate(&prog, &res).remove(0);
    opt::optimise(&mut f);
    for i in &f.code {
        println!("    {}", tac::show(&f, i));
    }
    let g = cfg::build(&f);
    let gr = regalloc::interference(&f, &g);
    let cost = regalloc::spill_costs(&f, &g);
    let name = |t: &u32| tac::val(&f, tac::Val::T(*t));
    println!("interference graph: {} nodes, {} edges", gr.adj.len(), gr.edges());
    for (t, ns) in &gr.adj {
        let v: Vec<String> = ns.iter().map(name).collect();
        println!("  {:<4} cost {:>4}  -- {}", name(t), cost[t], v.join(" "));
    }
    for k in ks {
        let c = regalloc::colour(&gr, k, &cost);
        let v: Vec<String> = c.colour.iter().map(|(t, c)| format!("{}:{c}", name(t))).collect();
        let s: Vec<String> = c.spilled.iter().map(name).collect();
        let s = if s.is_empty() { "none".to_string() } else { s.join(" ") };
        println!("k = {k}: {}   spilled: {s}", v.join(" "));
    }
}
