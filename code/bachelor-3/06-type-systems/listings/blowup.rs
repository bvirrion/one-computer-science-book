// blowup.rs -- a family of short programs whose principal types double
// in depth at each step: f(k) applies f(k-1) twice.
#![allow(dead_code)]
#[path = "../../05-lambda-calculus/listings/lam.rs"]
mod lam;
#[path = "unify.rs"]
mod unify;
#[path = "infer.rs"]
mod infer;
use lam::Ty;
use std::collections::HashMap;
use std::sync::atomic::Ordering;

/// let f0 = \x. (x, x) in let f1 = \x. f0 (f0 x) in ... in fn
fn program(n: usize) -> String {
    let mut src = String::from(r"let f0 = \x. (x, x) in ");
    for k in 1..=n {
        src += &format!(r"let f{k} = \x. f{} (f{} x) in ", k - 1, k - 1);
    }
    src + &format!("f{n}")
}

fn leaves(t: &Ty) -> u64 {
    match t {
        Ty::Fun(a, b) | Ty::Pair(a, b) => leaves(a) + leaves(b),
        _ => 1,
    }
}

/// Distinct subtrees: the size of the type drawn as a graph with sharing.
fn shared(t: &Ty, ids: &mut HashMap<(u8, usize, usize), usize>) -> usize {
    let key = match t {
        Ty::Var(v) => (0, *v as usize, 0),
        Ty::Pair(a, b) => (1, shared(a, ids), shared(b, ids)),
        Ty::Fun(a, b) => (2, shared(a, ids), shared(b, ids)),
        Ty::Int => (3, 0, 0),
        Ty::Bool => (4, 0, 0),
    };
    let next = ids.len();
    *ids.entry(key).or_insert(next)
}

fn main() {
    println!(" n  program  unify calls  leaves of the type  distinct subtrees");
    for n in 0..=4 {
        let src = program(n);
        unify::UNIFY_CALLS.store(0, Ordering::Relaxed);
        let t = infer::principal(&lam::parse(&src).unwrap()).unwrap();
        let Ty::Fun(_, result) = &t else { panic!("a function type") };
        let mut ids = HashMap::new();
        shared(result, &mut ids);
        println!("{n:>2}  {:>7}  {:>11}  {:>18}  {:>17}", src.len(),
                 unify::UNIFY_CALLS.load(Ordering::Relaxed), leaves(result), ids.len());
    }
}
