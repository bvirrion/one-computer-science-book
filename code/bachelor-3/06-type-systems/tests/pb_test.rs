// The weekend problem: the family f(k) = f(k-1) twice, and its types.
#![allow(dead_code)]
#[path = "../../05-lambda-calculus/listings/lam.rs"]
mod lam;
#[path = "../listings/unify.rs"]
mod unify;
#[path = "../listings/infer.rs"]
mod infer;
use lam::Ty;

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
fn depth(t: &Ty) -> u64 {
    match t {
        Ty::Fun(a, b) | Ty::Pair(a, b) => 1 + depth(a).max(depth(b)),
        _ => 0,
    }
}

#[test]
fn sizes_of_the_family() {
    for n in 0..=4u32 {
        let src = program(n as usize);
        assert_eq!(src.len(), 25 + 26 * n as usize);
        let t = infer::principal(&lam::parse(&src).unwrap()).unwrap();
        let Ty::Fun(a, r) = &t else { panic!() };
        assert_eq!(**a, Ty::Var(0));
        assert_eq!(leaves(r), 1u64 << (1u32 << n));
        assert_eq!(depth(r), 1u64 << n);
    }
}

#[test]
fn small_lets_by_hand() {
    let p = |s: &str| lam::show_ty(&infer::principal(&lam::parse(s).unwrap()).unwrap());
    assert_eq!(p(r"\x. (x, x)"), "'a -> 'a * 'a");
    assert_eq!(p(r"let f0 = \x. (x, x) in \x. f0 (f0 x)"), "'a -> ('a * 'a) * ('a * 'a)");
    assert_eq!(p(r"let f0 = \x. (x, x) in f0 (f0 1)"), "(int * int) * (int * int)");
}

#[test]
fn without_let_the_family_is_rejected() {
    // a lambda-bound f0 is monomorphic: f0 (f0 x) needs 'a = 'a * 'a
    assert!(infer::principal(&lam::parse(r"(\f0. \x. f0 (f0 x)) (\x. (x, x))").unwrap()).is_err());
}
