// The weekend problem: instructions executed by the compiled fib(n).
#![allow(dead_code)]
mod common;

fn fibonacci(k: u64) -> u64 {
    let (mut a, mut b) = (0, 1);
    for _ in 0..k {
        (a, b) = (b, a + b);
    }
    a
}

#[test]
fn instructions_are_39_f_minus_7() {
    let asm = std::fs::read_to_string("../listings/fib.S").unwrap();
    for n in 0..=20u64 {
        let r = common::rv_run(&asm, &[n as i32], 10_000_000);
        assert_eq!(r.output, format!("{}\n", fibonacci(n)));
        assert_eq!(r.instructions, 39 * fibonacci(n + 1) - 7, "n = {n}");
    }
}

#[test]
fn calls_are_2_f_minus_1() {
    // count the calls of fib by the recursion the code makes
    fn calls(n: u64) -> u64 { if n < 2 { 1 } else { 1 + calls(n - 1) + calls(n - 2) } }
    for n in 0..=25 {
        assert_eq!(calls(n), 2 * fibonacci(n + 1) - 1);
    }
}

#[test]
fn per_call_costs_from_the_code() {
    // leaf call: 11 instructions; inner call: 28; main alone: 21 (read in fib.S)
    let asm = std::fs::read_to_string("../listings/fib.S").unwrap();
    let body: Vec<&str> = asm.lines().collect();
    let pos = |l: &str| body.iter().position(|x| *x == l).unwrap();
    let (fib, main) = (pos("fib:"), pos("main:"));
    let fib_words = body[fib + 1..main].iter().filter(|l| l.starts_with("    ")).count();
    assert_eq!(fib_words, 33);
    let (leaf, inner, m) = (11u64, 28u64, 21u64);
    assert_eq!((leaf + inner, m as i64 - inner as i64), (39, -7));
}
