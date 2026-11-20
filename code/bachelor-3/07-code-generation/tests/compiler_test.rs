// Tests for chapter 7: the compiler agrees with the interpreter.
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
#[path = "../listings/tac.rs"]
mod tac;
#[path = "../listings/cfg.rs"]
mod cfg;
#[path = "../listings/frame.rs"]
mod frame;
#[path = "../listings/riscv.rs"]
mod riscv;
#[path = "../exercises/ex6_rem_neg.rs"]
mod ex6;
#[path = "../exercises/ex11_registers.rs"]
mod ex11;
#[path = "../exercises/ex12_oracle.rs"]
mod ex12;
mod common;

fn compile_with(src: &str, extra: Option<riscv::Extra>) -> Result<String, String> {
    let (p, r, _) = typecheck::check_source(src, "t.moor")?;
    riscv::program(&p, &tac::translate(&p, &r), extra)
}
fn compile(src: &str) -> String {
    compile_with(src, None).unwrap()
}
fn tac_of(src: &str) -> Vec<tac::FuncTac> {
    let (p, r, _) = typecheck::check_source(src, "t.moor").unwrap();
    tac::translate(&p, &r)
}

/// The commuting square: interpreter and compiled code agree.
fn agree(src: &str, input: &[i32], extra: Option<riscv::Extra>) -> common::RvRun {
    let (p, _, _) = typecheck::check_source(src, "t.moor").unwrap();
    let want = interp::run(&p, input, 10_000_000);
    let got = common::rv_run(&compile_with(src, extra).unwrap(), input, 10_000_000);
    assert_eq!(got.fault, "", "{src}");
    assert_eq!(got.output, want.output, "{src}");
    assert_eq!(got.exit, want.exit.clone().unwrap(), "{src}");
    got
}

#[test]
fn samples_agree_with_the_interpreter() {
    for f in ["fib.moor", "sum_array.moor", "primes.moor", "expr.moor"] {
        let src = std::fs::read_to_string(format!("../listings/{f}")).unwrap();
        let input: &[i32] = if f == "fib.moor" { &[12] } else { &[] };
        agree(&src, input, None);
    }
    for f in ["ok.moor", "sieve.moor"] {
        agree(&std::fs::read_to_string(format!("../../04-semantic-analysis/listings/{f}")).unwrap(), &[], None);
    }
    let fib = std::fs::read_to_string("../listings/fib.moor").unwrap();
    for n in 0..10 {
        agree(&fib, &[n], None);
    }
}

#[test]
fn fib_s_is_the_compiler_output() {
    let src = std::fs::read_to_string("../listings/fib.moor").unwrap();
    assert_eq!(compile(&src), std::fs::read_to_string("../listings/fib.S").unwrap());
}

#[test]
fn frames_of_fib_and_main() {
    let fs = tac_of(&std::fs::read_to_string("../listings/fib.moor").unwrap());
    let sizes: Vec<(u32, i32, i32)> = fs.iter().map(|f| {
        let fr = frame::Frame::new(f.temps);
        (f.temps, fr.size, fr.ra)
    }).collect();
    assert_eq!(sizes, [(6, 32, 28), (3, 16, 12)]);
    assert_eq!(frame::Frame::new(7).size, 32); // exercise 4: 4 * 7 + 4 = 32
    assert_eq!(frame::Frame::new(8).size, 48); // 36, rounded up
}

#[test]
fn exercise_1_tac_of_an_assignment() {
    let fs = tac_of("fn main() { var a = 2; var b = 3; var c = 4; var x = 0; x = a * b + c; }");
    let code: Vec<String> = fs[0].code.iter().map(|i| tac::show(&fs[0], i)).collect();
    assert_eq!(&code[4..7], ["t4 = a * b", "t5 = t4 + c", "x = t5"]);
}

#[test]
fn exercise_2_leaders() {
    let fs = tac_of("fn main() { var i = 0; while i < 3 { if i == 1 { print(i); } i = i + 1; } }");
    let ls = cfg::leaders(&fs[0].code);
    let code: Vec<String> = fs[0].code.iter().map(|i| tac::show(&fs[0], i)).collect();
    let starts: Vec<&str> = ls.iter().map(|&k| code[k].as_str()).collect();
    assert_eq!(starts, ["i = 0", "L1:", "goto L3", "L2:", "goto L5", "L4:", "L5:", "L6:", "L3:"]);
}

#[test]
fn exercise_3_sum_array_on_rv() {
    let src = std::fs::read_to_string("../listings/sum_array.moor").unwrap();
    let r = common::rv_run(&compile(&src), &[], 1_000_000);
    assert_eq!((r.output.as_str(), r.exit), ("285\n", 29));
}

#[test]
fn exercise_5_ra_not_saved() {
    let src = std::fs::read_to_string("../listings/fib.S").unwrap();
    let bug: String = src.lines().filter(|l| !l.contains(" ra, 28(sp)"))
        .map(|l| format!("{l}\n")).collect();
    assert_eq!(src.lines().count() - bug.lines().count(), 2);
    let r = common::rv_run(&bug, &[2], 100_000);
    assert_eq!(r.exit, -1);
    assert_eq!(r.fault, "store access fault at 0x80000010");
    assert_eq!(common::rv_run(&bug, &[1], 100_000).output, "1\n"); // no nested call: fine
}

#[test]
fn exercise_6_rem_and_neg() {
    let src = "fn main() -> int { var a = 17; var b = -5; print(a % 5); print(-a % b); print(a % 0); \
               print(-(a - 20)); return -a % 7 + 10; }";
    assert!(compile_with(src, None).unwrap_err().contains("exercise 6"));
    let r = agree(src, &[], Some(&ex6::select));
    assert_eq!(r.output, "2\n-2\n17\n3\n");
}

#[test]
fn exercise_7_instructions_for_an_increment() {
    let base = "array a[10]; fn main() { var i = 3; }";
    let inc = "array a[10]; fn main() { var i = 3; a[i] = a[i] + 1; }";
    let count = |s: &str| compile(s).lines().filter(|l| l.starts_with("    ")).count();
    let words = |s: &str| compile(s).lines().filter(|l| l.starts_with("    "))
        .map(|l| if l.trim_start().starts_with("la ") { 2 } else { 1 }).sum::<usize>();
    assert_eq!(count(inc) - count(base), 15);
    assert_eq!(words(inc) - words(base), 17);
}

#[test]
fn exercise_9_cfg_of_a_loop_with_return() {
    let fs = tac_of("fn f(n: int) -> int { while n > 0 { if n == 3 { return 1; } n = n - 1; } return 0; } \
                     fn main() { print(f(5)); }");
    let g = cfg::build(&fs[0]);
    let succ: Vec<Vec<usize>> = g.succ.clone();
    let want: [&[usize]; 10] = [&[2, 1], &[8], &[4, 3], &[6], &[], &[7], &[7], &[0], &[], &[]];
    assert_eq!(succ, want);
}

#[test]
fn exercise_11_register_need() {
    use ex11::E::{Leaf, Op};
    let l = || Box::new(Leaf);
    let balanced = Op(Box::new(Op(l(), l())), Box::new(Op(l(), l())));
    let left = Op(Box::new(Op(Box::new(Op(l(), l())), l())), l());
    let right = Op(l(), Box::new(Op(l(), Box::new(Op(l(), l())))));
    assert_eq!((ex11::need(&balanced), ex11::need(&left), ex11::need(&right)), (3, 2, 2));
    assert_eq!((ex11::left_first(&left), ex11::left_first(&right)), (2, 4));
}

#[test]
fn exercise_12_random_programs() {
    let mut steps = 0;
    for seed in 1..=60 {
        let src = ex12::program(seed);
        steps += agree(&src, &[], None).instructions;
    }
    assert!(steps > 0);
}

#[test]
fn rem_and_neg_are_refused_without_the_hook() {
    assert!(compile_with("fn main() { print(-1); }", None).is_ok()); // a negative literal is a constant
    assert!(compile_with("fn main() { var x = 1; print(-x); }", None).is_err());
}

#[test]
fn problem_loop_version_is_linear() {
    let src = std::fs::read_to_string("../exercises/pb_fibloop.moor").unwrap();
    let asm = compile(&src);
    for n in [0, 1, 2, 10, 20] {
        let r = agree(&src, &[n], None);
        assert_eq!(r.instructions, 19 * n as u64 + 39);
        assert_eq!(common::rv_run(&asm, &[n], 100_000).instructions, r.instructions);
    }
}
