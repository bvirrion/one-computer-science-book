// moorc_opt.rs -- the Moor compiler with optimisation levels.
// Usage: moorc_opt [-O0|-O1|-O2] [-k N] FILE.moor > FILE.S
//   -O0  chapter 7's code; -O1  optimised three-address code, every temporary
//   on the stack; -O2  the same, with registers allocated by colouring (k of them).
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
#[path = "rvgen.rs"]
mod rvgen;
#[path = "../../07-code-generation/listings/frame.rs"]
mod frame;
#[path = "../../07-code-generation/listings/riscv.rs"]
mod riscv;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let level = args.iter().find_map(|a| a.strip_prefix("-O")).unwrap_or("2").to_string();
    let k = args.iter().position(|a| a == "-k").map_or(12, |i| args[i + 1].parse().unwrap());
    let file = args.last().expect("usage: moorc_opt [-O0|-O1|-O2] [-k N] FILE.moor");
    let src = std::fs::read_to_string(file).expect("a readable file");
    let (prog, res, _) = typecheck::check_source(&src, file).unwrap_or_else(|m| {
        eprint!("{m}");
        std::process::exit(1)
    });
    let mut funcs = tac::translate(&prog, &res);
    if level != "0" {
        for f in &mut funcs {
            opt::optimise(f);
        }
    }
    let asm = match level.as_str() {
        "2" => Ok(rvgen::program(&prog, &funcs, k).0),
        _ => riscv::program(&prog, &funcs, None),
    };
    match asm {
        Ok(text) => print!("{text}"),
        Err(m) => {
            eprintln!("{m}");
            std::process::exit(1)
        }
    }
}
