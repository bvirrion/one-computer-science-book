// Tests for chapter 8: the optimised and allocated code agrees with the
// interpreter; the analyses give the sets the text and the solutions quote.
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
#[path = "../../04-semantic-analysis/listings/interp.rs"]
mod interp;
#[path = "../../07-code-generation/listings/tac.rs"]
mod tac;
#[path = "../../07-code-generation/listings/cfg.rs"]
mod cfg;
#[path = "../../07-code-generation/listings/frame.rs"]
mod frame;
#[path = "../../07-code-generation/listings/riscv.rs"]
mod riscv;
#[path = "../../07-code-generation/exercises/ex12_oracle.rs"]
mod oracle;
#[path = "../../07-code-generation/tests/common.rs"]
mod common;
#[path = "../listings/dataflow.rs"]
mod dataflow;
#[path = "../listings/liveness.rs"]
mod liveness;
#[path = "../listings/reaching.rs"]
mod reaching;
#[path = "../listings/ssa.rs"]
mod ssa;
#[path = "../listings/opt.rs"]
mod opt;
#[path = "../listings/regalloc.rs"]
mod regalloc;
#[path = "../listings/rvgen.rs"]
mod rvgen;
#[path = "../exercises/ex5_wrong_way.rs"]
mod ex5;
#[path = "../exercises/ex6_dead_store.rs"]
mod ex6;
#[path = "../exercises/ex12_licm.rs"]
mod ex12;


fn shown(f: &tac::FuncTac) -> Vec<String> {
    f.code.iter().map(|i| tac::show(f, i)).collect()
}

fn funcs(src: &str) -> (ast::Program, Vec<tac::FuncTac>) {
    let (p, r, _) = typecheck::check_source(src, "t.moor").unwrap();
    let fs = tac::translate(&p, &r);
    (p, fs)
}

/// Compile at a level: 0 naive, 1 optimised TAC, 2 optimised and allocated with k registers.
fn compile(src: &str, level: u32, k: usize) -> String {
    let (p, mut fs) = funcs(src);
    if level > 0 {
        for f in &mut fs { opt::optimise(f); }
    }
    if level == 2 { rvgen::program(&p, &fs, k).0 } else { riscv::program(&p, &fs, None).unwrap() }
}

fn agree(src: &str, input: &[i32], level: u32, k: usize) -> common::RvRun {
    let (p, _) = funcs(src);
    let want = interp::run(&p, input, 10_000_000);
    let got = common::rv_run(&compile(src, level, k), input, 10_000_000);
    assert_eq!(got.fault, "", "{src}");
    assert_eq!((got.output.as_str(), got.exit), (want.output.as_str(), want.exit.clone().unwrap()), "{src}");
    got
}

fn read(path: &str) -> String {
    std::fs::read_to_string(path).unwrap()
}

fn loans() -> Vec<i32> {
    let text = read("../../../../data/town/loans.csv");
    let day = |s: &str| {
        let v: Vec<i32> = s.split('-').map(|x| x.parse().unwrap()).collect();
        let (y, m, d) = (v[0], v[1], v[2]); // days since 2024-12-31, enough for 2025 and early 2026
        let before = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334][(m - 1) as usize];
        (y - 2025) * 365 + before + d
    };
    let mut days = vec![];
    for line in text.lines().skip(1) {
        let c: Vec<&str> = line.split(',').collect();
        if !c[5].is_empty() { days.push(day(c[5]) - day(c[4])); }
    }
    [vec![days.len() as i32], days].concat()
}

#[test]
fn every_level_agrees_with_the_interpreter() {
    let ch7 = "../../07-code-generation/listings/";
    let samples = [
        (read(&format!("{ch7}fib.moor")), vec![12]),
        (read(&format!("{ch7}sum_array.moor")), vec![]),
        (read(&format!("{ch7}primes.moor")), vec![]),
        (read(&format!("{ch7}expr.moor")), vec![]),
        (read("../../04-semantic-analysis/listings/ok.moor"), vec![]),
        (read("../../04-semantic-analysis/listings/sieve.moor"), vec![]),
        (read("../listings/loop.moor"), vec![]),
        (read("../listings/billing.moor"), loans()),
    ];
    for (src, input) in &samples {
        for (level, k) in [(0, 0), (1, 0), (2, 12), (2, 3), (2, 1)] {
            agree(src, input, level, k);
        }
    }
}

#[test]
fn random_programs_at_every_level() {
    for seed in 1..=60 {
        let src = oracle::program(seed);
        for (level, k) in [(1, 0), (2, 12), (2, 2)] {
            agree(&src, &[], level, k);
        }
    }
}

fn names(f: &tac::FuncTac, s: &liveness::Set) -> Vec<String> {
    s.iter().map(|&t| tac::val(f, tac::Val::T(t))).collect()
}

#[test]
fn exercise_1_live_variables_of_the_loop() {
    let (_, fs) = funcs(&read("../listings/loop.moor"));
    let (f, g) = (&fs[0], cfg::build(&fs[0]));
    let sol = dataflow::solve(&liveness::Liveness { code: &f.code, g: &g }, &g);
    let after = liveness::live_after(&f.code, &g, &sol.after);
    assert_eq!(sol.visits, 12);
    assert_eq!(names(f, &after[0]), ["n", "s"]);       // after s = 0
    assert_eq!(names(f, &after[7]), ["n", "s", "i", "sq"]); // after sq = t3
    assert_eq!(names(f, &after[10]), ["n", "s", "t6"]); // after t6 = i + 1
    assert_eq!(names(f, &sol.before[0]), ["n"]);
}

#[test]
fn exercise_2_dominators() {
    let src = "fn f(n: int) -> int { while n > 0 { if n == 3 { return 1; } n = n - 1; } return 0; } \
               fn main() { print(f(5)); }";
    let (_, fs) = funcs(src);
    let g = cfg::build(&fs[0]);
    let dom = ssa::dominators(&g);
    let id = ssa::idom(&dom);
    let want: [&[usize]; 10] = [&[0], &[0, 1], &[0, 2], &[0, 2, 3], &[0, 2, 4], &[], &[0, 2, 3, 6],
                                &[0, 2, 3, 6, 7], &[0, 1, 8], &[]];
    for b in 0..10 {
        assert_eq!(dom[b].iter().copied().collect::<Vec<_>>(), want[b], "B{b}");
    }
    assert_eq!(id, [None, Some(0), Some(0), Some(2), Some(2), None, Some(3), Some(6), Some(1), None]);
}

#[test]
fn exercise_3_phi_placement() {
    let src = "fn f(n: int) -> int { var x = 0; var y = 1; if n > 0 { x = n; } else { y = n; } \
               while x < 10 { x = x + y; } return x; } fn main() { print(f(3)); }";
    let (_, fs) = funcs(src);
    let g = cfg::build(&fs[0]);
    let s = ssa::to_ssa(&fs[0], &g);
    let all: Vec<&String> = s.phis.iter().flatten().collect();
    assert_eq!(all, ["x.2 = phi(B3: x.0, B2: x.1)", "y.2 = phi(B3: y.1, B2: y.0)", "x.3 = phi(B4: x.2, B7: x.4)"]);
}

#[test]
fn exercise_4_folded_tac() {
    let src = "fn main() -> int { var a = 6; var b = a * 7; var c = b - 40; \
               if c > 1 { print(b); } else { print(a); } return c * a; }";
    let (_, mut fs) = funcs(src);
    assert_eq!(opt::optimise(&mut fs[0]), 3);
    assert_eq!(shown(&fs[0]), ["L1:", "call print(42)", "L3:", "return 12"]);
}

#[test]
fn exercise_5_liveness_the_wrong_way() {
    let (_, fs) = funcs(&read("../listings/loop.moor"));
    let (f, g) = (&fs[0], cfg::build(&fs[0]));
    let w = dataflow::solve(&ex5::WrongWay { code: &f.code, g: &g }, &g);
    assert!(w.before[0].is_empty()); // n would be dead at the entry
    assert_eq!(names(f, &w.after[4]), ["n", "s", "i"]); // and s, i live after the return
}

#[test]
fn exercise_6_dead_stores() {
    let src = "var g: int = 0; var h: int = 0; \
               fn main() -> int { g = 1; h = 2; g = 3; print(g); g = 4; h = g; g = 5; return g + h; }";
    let (_, mut fs) = funcs(src);
    assert_eq!(ex6::dead_stores(&mut fs[0]), 1);
    assert_eq!(shown(&fs[0])[..2], ["h = 2", "g = 3"]);
    let (p, _) = funcs(src);
    let out = common::rv_run(&riscv::program(&p, &fs, None).unwrap(), &[], 10_000);
    assert_eq!((out.output.as_str(), out.exit), ("3\n", 9));
}

#[test]
fn exercise_8_three_registers_are_not_enough() {
    let (_, mut fs) = funcs(&read("../listings/loop.moor"));
    opt::optimise(&mut fs[0]);
    let (f, g) = (&fs[0], cfg::build(&fs[0]));
    let gr = regalloc::interference(f, &g);
    let cost = regalloc::spill_costs(f, &g);
    let clique: Vec<u32> = ["n", "s", "i", "t3"].iter()
        .map(|x| *f.names.iter().find(|(_, n)| n == x).map(|(t, _)| t).unwrap_or(&3)).collect();
    for a in &clique {
        for b in &clique {
            assert!(a == b || gr.adj[a].contains(b));
        }
    }
    let three = regalloc::colour(&gr, 3, &cost);
    assert_eq!(names(f, &three.spilled), ["n"]);
    assert!(regalloc::colour(&gr, 4, &cost).spilled.is_empty());
}

#[test]
fn exercise_9_phis_of_nested_loops() {
    for d in 1..=5usize {
        let mut body = String::from("s = s + 1;");
        for k in (0..d).rev() {
            body = format!("var i{k} = 0; while i{k} < 3 {{ {body} i{k} = i{k} + 1; }}");
        }
        let (_, fs) = funcs(&format!("fn main() -> int {{ var s = 0; {body} return s; }}"));
        let g = cfg::build(&fs[0]);
        assert_eq!(ssa::to_ssa(&fs[0], &g).count, d * (d + 3) / 2, "depth {d}");
    }
}

#[test]
fn exercise_10_not_distributive() {
    let src = "fn main() -> int { var c = read(); var a = 0; var b = 0; \
               if c > 0 { a = 2; b = 3; } else { a = 3; b = 2; } var x = a + b; print(x); return 0; }";
    let (_, mut fs) = funcs(src);
    opt::optimise(&mut fs[0]);
    assert!(shown(&fs[0]).contains(&"t4 = a + b".to_string())); // 5 on every path, not found
}

#[test]
fn exercise_12_loop_invariant_code_motion() {
    let src = "fn main() -> int { var a = read(); var b = read(); var s = 0; var i = 0; \
               while i < 100 { s = s + a * b + i; i = i + 1; } print(s); return 0; }";
    let (p, mut fs) = funcs(src);
    opt::optimise(&mut fs[0]);
    let before = common::rv_run(&riscv::program(&p, &fs, None).unwrap(), &[6, 7], 100_000);
    assert_eq!(ex12::hoist(&mut fs[0]), 1);
    assert_eq!(shown(&fs[0])[4..6], ["t6 = t0 * t2", "L1:"]);
    let after = common::rv_run(&riscv::program(&p, &fs, None).unwrap(), &[6, 7], 100_000);
    assert_eq!((before.output.as_str(), after.output.as_str()), ("9150\n", "9150\n"));
    assert_eq!(before.instructions - after.instructions, 396); // 4 per iteration, 4 once
}

#[test]
fn reaching_definitions_of_the_loop() {
    let (_, fs) = funcs(&read("../listings/loop.moor"));
    let (f, g) = (&fs[0], cfg::build(&fs[0]));
    let r = dataflow::solve(&reaching::Reaching { code: &f.code, g: &g }, &g);
    let header: Vec<usize> = r.before[1].iter().copied().collect();
    assert_eq!(header, [0, 1, 6, 7, 8, 9, 10, 11]);
}

#[test]
fn problem_billing_counts() {
    let src = read("../listings/billing.moor");
    let input = loans();
    assert_eq!(input[0], 378);
    let run = |level, k| agree(&src, &input, level, k);
    let (o1, k12) = (run(1, 0), run(2, 12));
    assert_eq!((o1.instructions, k12.instructions), (21496, 11815));
    let shown = common::rv_run(&compile(&src, 2, 12), &input, 1_000_000);
    assert_eq!(shown.output, "87\n24305\n500\n");
}
